import pandas as pd
import numpy as np

# Function to load data from a file path
def load_data(file_path):
    
    df = pd.read_csv(file_path)

    new_column_names = ['Date'] + list(df.columns[1:-24]) + list(range(1, 25))
    df.columns = new_column_names
    
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    
    df.replace(-9999, np.nan, inplace=True)

    return df