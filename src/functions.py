# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:08:51 2022

@author: Jaime García Chaparr
"""

import pandas as pd
from pandas.plotting import autocorrelation_plot
import numpy as np

from datetime import datetime as dt

from sklearn.metrics import mean_squared_error as mse

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA

#%% Generate forecasts

def evaluate_forecasts(ts, 
                      exog = None,
                      region_name = None,
                      break_year = 2016,
                      max_pred_year = 2025,
                      plot = False,
                      ps = [i for i in range(6)],
                      ds = [i for i in range(2)],
                      qs = [i for i in range(6)]):
    
    """Generates ARIMA models with the specified parameters.
    It evaluates all parameters and retains the model with the least
    RMSE.
    
    Returns `region_forecast` -> dictionary:
        - region_name
        - forecast: predicted population values and confidence interval.
        - order: hyperparameters of the optimal model.
        - rmse: training RMSE of the optimal model."""
        
# =============================================================================
#     def replace_negatives(array):
#         """Replaces negatives by 0 for population forecasts."""
#         
#         array[array < 0] = 0    
#     
#         return array
# =============================================================================

    print(f'Generating model for {region_name}')
    
    # Generate splits    
    break_time = dt(break_year, 12, 31)
    ts_train = ts[ts.index <= break_time]
    ts_test = ts[ts.index > break_time]

    # Prepare hyperparameter counts
    best_model = None
    min_rmse = 1e6
    
    # Adjust hyperparameters to select the best model
    for p in ps:
        for d in ds:
            for q in qs:
                try:
                    print(f'Testing for ({p}, {d}, {q})')
                    
                    # Initialize model
                    sarimax = ARIMA(ts_train, 
                                      #exog = exog,
                                      order = (p, d, q))
                    res = sarimax.fit()
                        
                    # Get and evaluate predictions
                    ts_pred = res.predict(start = dt(break_year + 1, 12, 31), 
                                          end = dt(2021, 12, 31))
                    #ts_pred = replace_negatives(ts_pred)
                    rmse = mse(ts_test, ts_pred, squared = False)
                    
                    # Compare model with temporary best
                    if rmse < min_rmse:
                        best_model = sarimax
                        min_rmse = rmse
                except:
                    print('Error')
                    pass
                
    # Compute forecasts for best model
    # bm = best model
    bm_res = best_model.fit()
    bm_pred = bm_res.get_prediction(start = dt(2022, 1, 1), 
                                      end = dt(max_pred_year, 1, 1)).summary_frame()
    print(bm_pred)
    
    
    if plot:
        bm_pred['mean'].plot(c = 'b')
        ts_test.plot(c = 'g')
        bm_pred['mean_ci_lower'].plot(c = 'r') 
        bm_pred['mean_ci_upper'].plot(c = 'r');

    
    # Build final dictionary

    region_forecast = {
                        'region' : region_name,
                        'forecast' : bm_pred,
                        'order' : best_model.order,
                        'rmse' : min_rmse
                        }        
    print(region_forecast)
    
    return region_forecast
    
    
                



