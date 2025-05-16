
# Pipeline

First of all, install all the requirements by running this command:

```bash
pip install -r requirements.txt
```

The `pipeline` directory contains three Python files: `data_ingestion.py`, `data_cleaning.py`, and `data_loading.py`.

Run the following commands in the same order one by one:

### 🔁 How to Run the Pipeline

To run the pipeline, go to the **Run Pipeline** page from the Streamlit sidebar and click the **"Run Data Pipeline"** button.

This will:
- Automatically download match data in JSON format.
- Clean and extract match-level information.
- Add synthetic features like **weather** and **toss alignment**.
- Save the final dataset in a SQLite database named `final_data.db`.

🧹 Temporary folders are deleted after processing to keep the workspace clean.