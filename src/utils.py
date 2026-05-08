import pandas as pd

def swap_decimal_separator(value, process_percentage=True):
    if pd.isna(value) or value == '':
        return value
    value_format = str(value).replace('.', ',')
    return f'{value_format}%' if process_percentage else value_format