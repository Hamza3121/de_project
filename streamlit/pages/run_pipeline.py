
import streamlit as st
import subprocess
import os
import time
import sys

st.set_page_config(page_title="🛠️ Run Data Pipeline", layout="centered")
st.title("🛠️ Data Pipeline Runner")

st.write("Click the button below to run the full data ingestion and cleaning pipeline.")

if st.button("Run Data Pipeline"):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    orchestration_path = os.path.join(base_dir, "pipeline", "orchestration.py")

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
