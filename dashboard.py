import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Fraud Monitor", layout="wide")
st.title("🛡️ Real-Time Fraud Detection Dashboard")

# Create a UI placeholder that we can refresh
dashboard_placeholder = st.empty()

while True:
    try:
        df = pd.read_csv("fraud_data.csv")
        
        with dashboard_placeholder.container():
            # 1. Metric Row
            col1, col2, col3 = st.columns(3)
            total = len(df)
            frauds = len(df[df['prediction'] == 'FRAUD'])
            
            col1.metric("Total Transactions", total)
            col2.metric("Fraud Cases", frauds, delta=frauds, delta_color="inverse")
            col3.metric("System Status", "Connected ✅")

            # 2. The Data Table
            st.subheader("Live Transaction Stream")
            # Show newest transactions first
            st.dataframe(df.iloc[::-1], use_container_width=True)
            
    except Exception:
        st.warning("Waiting for data stream to start...")
    
    time.sleep(2) # Refresh every 2 seconds