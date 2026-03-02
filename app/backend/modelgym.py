"""
--- modelgym ---

This module is responsible for training the model on the dataset
It also gets metrics for the model after training. 
"""
# Foreign imports:
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import root_mean_squared_error, r2_score

def separate_feature_and_target(df, target_col):
    """
    Takes a df and a target column
    Returns two df one with just features and one with just target columns
    """
    X = df.drop(columns=target_col)
    y = df[target_col]
    return X, y


def get_trained_model_and_metrics(df):
    """
    Takes a dataframe with features
    returns a trained model, and metrics
    """

    X,y = separate_feature_and_target(df, 'Price')
    
    tscv = TimeSeriesSplit(n_splits=18)

    # Store the score for averages:
    rf_rmse_scores = []
    rf_r2_scores = []

    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        model = LinearRegression() # makes a new model each time, deleting the old, the final model remains
        model.fit(X_train, y_train)
        
        pred = model.predict(X_test)
        rmse = root_mean_squared_error(y_test, pred)
        r2 = r2_score(y_test, pred)
        rf_rmse_scores.append(rmse)
        rf_r2_scores.append(r2)

     
    mean_rmse= np.mean(rf_rmse_scores)
    mean_r2 = np.mean(rf_r2_scores)
    metrics = (mean_rmse, mean_r2)
    
    return model, metrics
