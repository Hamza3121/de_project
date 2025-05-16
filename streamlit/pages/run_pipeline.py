
import streamlit as st
import subprocess
import os
import time
import sys
import sqlite3
import pandas as pd


st.set_page_config(page_title="🛠️ Pipeline and DB", layout="centered")
st.markdown("---")
st.subheader("📊 View Final DB Data")

if st.button("Show Match Data from DB"):
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "final_data.db"))

    if not os.path.exists(db_path):
        st.error("❌ Database not found at expected location.")
    else:
        try:
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT * FROM matches LIMIT 100", conn)
            conn.close()

            st.success("✅ Data loaded successfully!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Failed to read from database: {e}")

st.title("🛠️ Data Pipeline Runner")

st.write("Click the button below to run the full data ingestion and cleaning pipeline.")

if st.button("Run Data Pipeline"):
    # Get full path to orchestration.py in pipeline/
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    orchestration_path = os.path.join(project_root, "pipeline", "orchestration.py")

    with st.spinner("🔄 Running data pipeline... Please wait."):
        result = subprocess.run([sys.executable, orchestration_path], capture_output=True, text=True)
        time.sleep(1.5)

    if result.returncode != 0:
        st.error("❌ Pipeline failed")
        st.text("stdout:")
        st.code(result.stdout or "No stdout")
        st.text("stderr:")
        st.code(result.stderr or "No stderr")
    else:
        st.success("✅ Pipeline completed successfully!")
        st.code(result.stdout)
