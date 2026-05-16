import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Fraud Monitor", layout="wide")
st.title("🛡️ Real-Time Fraud Detection Dashboard")

# Create a UI placeholder that we can refresh
dashboard_placeholder = st.empty()

while True:
    try:
        # read_csv can occasionally fail if the consumer is writing to it at the exact same millisecond.
        # using errors='ignore' or catching it keeps the UI smooth.
        df = pd.read_csv("fraud_data.csv")
        
        with dashboard_placeholder.container():
            # 1. Metric Row
            col1, col2, col3 = st.columns(3)
            total = len(df)
            frauds = len(df[df['prediction'] == 'FRAUD'])
            
            # Calculate fraud rate percentage
            fraud_rate = (frauds / total * 100) if total > 0 else 0
            
            col1.metric("Total Transactions", f"{total:,}")
            col2.metric("Fraud Cases Detected", frauds, delta=f"{fraud_rate:.1f}% Rate", delta_color="inverse")
            col3.metric("System Status", "Connected ✅")

            # 2. Live Transaction Stream Layout Optimization
            st.subheader("Live Transaction Stream (Latest Events First)")
            
            # --- NEW: Filter columns for a clean view ---
            # We don't want to show V1 through V28 to the human operator! 
            # We filter for the human-readable operational columns.
            display_cols = ['timestamp', 'user_id', 'Amount', 'prediction']
            
            # Ensure the columns exist before filtering to avoid initialization errors
            available_cols = [col for col in display_cols if col in df.columns]
            
            if available_cols:
                # Reverse the dataframe to show newest first, and slice to the last 100 
                # rows so your browser's RAM doesn't crash after an hour of streaming!
                df_display = df[available_cols].iloc[::-1].head(100)
                
                # Apply a nice red/green highlight to the prediction column
                def highlight_fraud(val):
                    color = '#ffcccc' if val == 'FRAUD' else '#ccffcc'
                    return f'background-color: {color}'
                
                st.dataframe(
                    df_display.style.map(highlight_fraud, subset=['prediction']),
                    use_container_width=True
                )
            else:
                st.info("Synchronizing data stream columns...")
                
    except Exception as e:
        # Keeps the dashboard alive during cold starts when the CSV file hasn't been created yet
        st.warning("Waiting for live data stream to populate CSV...")
    
    time.sleep(2) # Refresh every 2 seconds