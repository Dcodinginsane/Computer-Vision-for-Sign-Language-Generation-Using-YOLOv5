# data_ingestion.py
import pandas as pd

def load_excel_data(file_path):
    """Load each sheet from an Excel workbook as a DataFrame."""
    excel_data = pd.ExcelFile(file_path)
    sheets_data = {sheet_name: excel_data.parse(sheet_name) for sheet_name in excel_data.sheet_names}
    return sheets_data

