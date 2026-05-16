import os
import joblib
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler # Added
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
import kagglehub

def train_model():
    # 1. Download and Load Dataset
    print("📦 Downloading dataset from Kaggle...")
    download_path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
    csv_path = os.path.join(download_path, "creditcard.csv")
    
    if not os.path.exists(csv_path):
        files = [f for f in os.listdir(download_path) if f.endswith('.csv')]
        csv_path = os.path.join(download_path, files[0])

    df = pd.read_csv(csv_path)
    X = df.drop(columns=['Class'])
    y = df['Class']
    
    # 2. Extract and Save Min/Max Boundaries for the Synthetic Producer
    bounds = {}
    for col in X.columns:
        bounds[col] = {"min": float(X[col].min()), "max": float(X[col].max())}
    
    os.makedirs("models", exist_ok=True)
    with open("models/feature_bounds.json", "w") as f:
        json.dump(bounds, f, indent=4)
    print("📊 Saved exact feature min/max boundaries to models/feature_bounds.json")

    # 3. Define Models and Tuning Grids
    model_configs = {
        "Logistic_Regression": {
            "model": LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1),
            "grid": {"C": [0.1, 1.0]}
        },
        "Random_Forest": {
            "model": RandomForestClassifier(random_state=42, n_jobs=-1),
            "grid": {"n_estimators": [10, 20], "max_depth": [10, 20]}
        },
        "XGBoost": {
            "model": XGBClassifier(random_state=42, eval_metric='logloss', n_jobs=-1),
            "grid": {"n_estimators": [30, 50], "max_depth": [3, 5]}
        }
    }
    
    # 4. 5-Fold Stratified Cross-Validation
    print("\n🔄 Starting 5-Fold Cross-Validation with Scaling & SMOTE...")
    cv_outer = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    best_overall_f1 = 0
    best_model_name = None
    best_tuned_params = None

    for name, config in model_configs.items():
        print(f"\n--- Tuning {name} ---")
        oof_preds = np.zeros(len(X))
        chosen_params_list = []

        for train_idx, val_idx in cv_outer.split(X, y):
            X_train_fold, X_val_fold = X.iloc[train_idx], X.iloc[val_idx]
            y_train_fold, y_val_fold = y.iloc[train_idx], y.iloc[val_idx]
            
            # Scale features within the fold to prevent leakage
            scaler_fold = MinMaxScaler()
            X_train_scaled = pd.DataFrame(scaler_fold.fit_transform(X_train_fold), columns=X.columns)
            X_val_scaled = pd.DataFrame(scaler_fold.transform(X_val_fold), columns=X.columns)
            
            # Apply SMOTE to scaled data
            smote = SMOTE(random_state=42)
            X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train_fold)
            
            # Internal Grid Search
            grid_search = GridSearchCV(
                estimator=config["model"], param_grid=config["grid"],
                cv=3, scoring='f1', n_jobs=-1
            )
            grid_search.fit(X_train_res, y_train_res)
            chosen_params_list.append(grid_search.best_params_)
            
            best_fold_model = grid_search.best_estimator_
            oof_preds[val_idx] = best_fold_model.predict(X_val_scaled)
        
        score = f1_score(y, oof_preds)
        print(f"📈 {name} CV F1 Score: {score:.4f}")
        
        if score > best_overall_f1:
            best_overall_f1 = score
            best_model_name = name
            best_tuned_params = chosen_params_list[-1]

    print(f"\n🏆 CHAMPION: {best_model_name} (F1: {best_overall_f1:.4f})")

    # 5. Final Full Train, Fit Scaler, and Serialize
    print("⚡ Fitting final MinMaxScaler and training champion on full balanced dataset...")
    
    # Save the final production scaler instance
    final_scaler = MinMaxScaler()
    X_scaled_full = pd.DataFrame(final_scaler.fit_transform(X), columns=X.columns)
    
    smote_final = SMOTE(random_state=42)
    X_resampled, y_resampled = smote_final.fit_resample(X_scaled_full, y)
    
    champion_base = model_configs[best_model_name]["model"].__class__
    final_model = champion_base(**best_tuned_params, random_state=42, n_jobs=-1)
    final_model.fit(X_resampled, y_resampled)
    final_model.feature_names_in_ = X.columns.to_numpy()
    
    # Save BOTH artifacts
    joblib.dump(final_model, "models/fraud_model.pkl")
    joblib.dump(final_scaler, "models/scaler.pkl") # Exporting the scaler
    print("✅ Model saved to models/fraud_model.pkl and Scaler saved to models/scaler.pkl")

if __name__ == "__main__":
    train_model()