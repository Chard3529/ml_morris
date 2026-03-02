"""
--- data_fetch_clean ---
This module is responsible for fetching data from source,
cleaning the data and making it available for other modules. 

In a real production environment this would fetch data from an api.
"""

# Foreign Imports:
import pandas as pd

# The path will always be this as this is the structure that is copied from the container
PATH = './backend/raw_data/Weekly_U.S._Regular_All_Formulations_Retail_Gasoline_Prices.csv'

# Pretend to get this csv file from api
def read_data():
    """
    Reads data from a csv file at a specific preset path 
    it reads in a way where we get just the data no headers 
    returns a dataframe
    """
    df = pd.read_csv(
        PATH, 
        skiprows=5, # skip 5 rows because the csv contains no data in first 5 rows
        header=None # to avoid first row in dataset becoming the header
        )
    return df
    

def clean_data_frame(df):
    """
    Takes a raw df for us-gas prices 
    returns a correctly formatted dataframe
    """
    
    df = df.copy()

    # Create new columns with names:
    df['Date'] = df.iloc[:,0]
    df['Price'] = df.iloc[:,1]

    # Drop first and second column
    df = df.drop(columns={df.columns[0], df.columns[1]})

    # Convert to correct values
    df['Date'] = pd.to_datetime(df['Date'])
    df['Price'] = pd.to_numeric(df['Price'])

    # Drop potential null values ( Since the file is local I know there are none)
    df = df.dropna()

    # Set Date as index:
    df = df.set_index('Date')

    # Sort the dataframe in ascending order 
    df = df.sort_index(ascending=True)
    return df


def fetch_clean_data():
    '''
    Calls the other functions and returns a prepared dataframe
    '''
    df = read_data()
    df = clean_data_frame(df)
    return df
