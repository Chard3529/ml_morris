"""
--- features ---

This module is responsible for adding features to the data.
"""

# Foreign imports:
import pandas as pd

def add_lagged_features(df, target_col, lags, final_week_pred):
    """
    Takes a df, a target and a tuple of lags
    Returns dataframe with features added
    """
    df = df.copy()
    for lag in lags:
        df[f'Lagged_{lag}'] = df[target_col].shift(lag)

    if not final_week_pred: 
        df = df.dropna()

    return df

def add_rolling_features(df, target_col, windows, final_week_pred):
    """
    Takes a df, target_col and windows of x weeks 
    Returns a dataframe with rolling features according to windows set
    """
    df = df.copy()
    for w in windows:
        df[f'Roll_mean_{w}'] = df[target_col].shift(1).rolling(w).mean()
        df[f'Roll_std_{w}'] = df[target_col].shift(1).rolling(w).std()
        df[f'Roll_min_{w}'] = df[target_col].shift(1).rolling(w).min()
        df[f'Roll_max_{w}'] = df[target_col].shift(1).rolling(w).max()
    if not final_week_pred:
        df = df.dropna()
    return df


def add_features(df,target_col='Price', lags=(1,2,3), windows=(2,3), final_week_pred=False):
    """
    Takes a df, optional: target_col: string, lags: tuple(int), windows: tuple(int)
    standard are: target_col='Price', lags=(1,2,3), windows=(2,3)
    returns df with features added 
    """
    df = df.copy()
    df = add_lagged_features(df,target_col,lags, final_week_pred)
    df = add_rolling_features(df,target_col,windows, final_week_pred)
    return df

