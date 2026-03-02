"""
--- Predictor ---
This module acts as the interface between the llm and the modules
It handles the main logic loop of the application, as well as communication with the llm
"""

# Foreign imports
import pandas as pd
import numpy as np

# Our imports
from .data_fetch_clean import fetch_clean_data
from .features import add_features
from .modelgym import get_trained_model_and_metrics


# Stored variables:
lags = (1,2,3)
windows = (2,3)

model = None 
metrics = None
test_X = None
cleaned_data = None


def train_and_set_model_and_data():
    """
    Calls functions from other modules, and sets the 
    variables model, metrics and test_X
    """
    global model, metrics, test_X, cleaned_data
    cleaned_data = fetch_clean_data()
    df = add_features(cleaned_data,lags=lags,windows=windows)
    model, metrics  = get_trained_model_and_metrics(df)
    

# Runs when this library is first imported, training and setting the model once,
# After the trained model is ready to be used again. 
train_and_set_model_and_data()

def get_model_metrics():
    """
    Returns the metrics for the current model
    """
    return metrics

def predict_gas_price_next_week():
    """
    This function predicts the gas price for next week.
    In this demo the current week is the week that starts monday 11-24-2025
    The next week is the week that starts monday 01-12-2025
    """
    largest_lag = max(lags)
    largest_window = max(windows)
    number_of_rows = max(largest_lag, largest_window)

    current_df = cleaned_data.tail(number_of_rows).copy()
    
    next_week = pd.to_datetime(current_df.index.max()) + pd.Timedelta(weeks=1) 

    current_df.loc[next_week] = np.nan
    
    current_df = add_features(current_df,lags=lags,windows=windows,final_week_pred=True)
    current_df = current_df.drop(columns = 'Price')
    
    feature_next_week = current_df.tail(1).copy()
    prediction = model.predict(feature_next_week)
    return float(prediction[0])
    


