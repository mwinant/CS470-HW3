"Helper Functions for CSP Algorithm."
import pandas as pd


def create_csp_data_from_csv(csv_file_path):
    """Read CSV file into a Dataframe."""
    return pd.read_csv(csv_file_path, index_col=0)


def create_restrictions_dict(csp_data):
    """Parse dataframe into dictionary containing variable constraints."""
    elements = csp_data.columns
    restrictions_dictionary: dict = {}
    for col in elements:
        for row in elements:
            if row == col:
                continue
            value = csp_data.at[col, row]
            if pd.isna(value):
                value = csp_data.at[row, col]
            if value == 1.0:
                restrictions_dictionary[(col, row)] = value
    return restrictions_dictionary
