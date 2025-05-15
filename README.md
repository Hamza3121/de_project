
# Pipeline

First of all, install all the requirements by running this command:

```bash
pip install -r requirements.txt
```

The `pipeline` directory contains three Python files: `data_ingestion.py`, `data_cleaning.py`, and `data_loading.py`.

Run the following commands in the same order one by one:

### 1: Data Ingestion

```bash
python pipeline/data_ingestion.py
```

- This will create a new directory named `raw_data` and save all the international matches data of these three formats: **Tests**, **ODIs**, and **T20Is**.

### 2: Data Cleaning

```bash
python pipeline/data_cleaning.py
```

- This will create a new directory named `clean_data` where it will save each format’s data into a separate file, containing **only match-level data**.

### 3: Data Loading

```bash
python pipeline/data_loading.py
```

- This will generate a CSV file named `final_data.csv` which contains **all formats’ data combined into a single file**.
