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
                      #exog = None,
                      region_name = None,
                      break_year = 2016,
                      max_pred_year = 2030,
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
                                          end = dt(ts.index[-1].year, 12, 31))
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
    bm_pred = bm_res.get_prediction(start = dt(ts.index[-1].year + 1, 12, 31), 
                                      end = dt(max_pred_year, 12, 31)).summary_frame()
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
    

#%% Evañute mod

def evaluate_forecasts_2(ts, 
                      #exog = None,
                      region_name = None,
                      break_year = 2016,
                      max_pred_year = 2030,
                      plot = False,
                      ps = [i for i in range(1, 7)],
                      ds = [i for i in range(2)],
                      qs = [i for i in range(4)],
                      trends = [None, 'c', 't']):
    
    """Generates ARIMA models with the specified parameters.
    It evaluates all parameters and retains the model with the least
    RMSE.
    
    Returns `region_forecast` -> dictionary:
        - region_name
        - forecast: predicted population values and confidence interval.
        - order: hyperparameters of the optimal model.
        - rmse: training RMSE of the optimal model."""

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
                for tr in trends:
                    try:
                        print(f'Testing for ({p}, {d}, {q}, {tr})')
                        
                        # Initialize model
                        arima = ARIMA(ts_train, 
                                          order = (p, d, q),
                                          trend = tr)
                        res = arima.fit()
                            
                        # Get and evaluate predictions
                        ts_pred = res.predict(start = dt(break_year + 1, 12, 31), 
                                              end = dt(ts.index[-1].year, 12, 31))
                        #ts_pred = replace_negatives(ts_pred)
                        rmse = mse(ts_test, ts_pred, squared = False)
                        
                        # Compare model with temporary best
                        if rmse < min_rmse:
                            best_model = arima
                            min_rmse = rmse
                    except:
                        print('Error')
                        pass
                    
    # Compute forecasts for optimal model
    optimal_arima = ARIMA(ts,
                          order = best_model.order,
                          trend = best_model.trend)
    om_res = optimal_arima.fit()
    print(best_model.order)
    
    om_pred = om_res.get_prediction(start = dt(ts.index[-1].year + 1, 12, 31), 
                                      end = dt(max_pred_year, 12, 31)).summary_frame()
    print(om_pred)
    
    
    if plot:
        om_pred['mean'].plot(c = 'b')
        ts_test.plot(c = 'g')
        om_pred['mean_ci_lower'].plot(c = 'r') 
        om_pred['mean_ci_upper'].plot(c = 'r');

    
    # Build final dictionary

    region_forecast = {
                        'region' : region_name,
                        'forecast' : om_pred,
                        'order' : best_model.order,
                        'rmse' : min_rmse
                        }        
    print(region_forecast)
    
    return region_forecast

    
#%% Compare ARIMA and ARIMAX

def evaluate_forecasts_sarimax(endog, exog,
                      region_name = None,
                      start_year = 2002,
                      break_year = 2016,
                      max_pred_year = 2030,
                      plot = False,
                      ps = [i for i in range(1, 7)],
                      ds = [i for i in range(2)],
                      qs = [i for i in range(1, 4)],
                      trends = [None, 't']):
    
    """Generates ARIMAX models with the specified parameters.
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
    
    # Endogenous variable
    endog_train = endog[endog.index <= break_time]
    endog_test= endog[endog.index > break_time]

    # Exogenous variables
    exog_train = exog[(exog.index <= break_time) &
                      (exog.index >= dt(start_year, 12, 31))]
    exog_test = exog[(exog.index > break_time) &
                     (exog.index <= dt(endog.index[-1].year, 12, 31))]
    
    exog_full_train = exog[(exog.index >= dt(start_year, 12, 31)) &
                           (exog.index <= dt(endog.index[-1].year, 12, 31))]
    
    exog_pred = exog[exog.index > dt(endog.index[-1].year, 12, 31)]

    # Prepare hyperparameter counts
    best_model = None
    min_rmse = 1e6
    
    # Adjust hyperparameters to select the best model
    for p in ps:
        for d in ds:
            for q in qs:
                for tr in trends:
                    try:
                        print(f'Testing for ({p}, {d}, {q}, {tr})')
                        
                        # Initialize model
                        sarimax = SARIMAX(endog_train, 
                                          exog = exog_train,
                                          order = (p, d, q),
                                          trend = tr)
                        res = sarimax.fit()
                            
                        # Get and evaluate predictions
                        endog_pred = res.predict(exog = exog_test,
                            start = dt(break_year + 1, 12, 31), 
                                              end = dt(endog.index[-1].year, 12, 31))
                        #ts_pred = replace_negatives(ts_pred)
                        rmse = mse(endog_test, endog_pred, squared = False)
                        
                        # Compare model with temporary best
                        if rmse < min_rmse:
                            best_model = sarimax
                            min_rmse = rmse
                            
                    except:
                        print('Error')
                        pass
                    
    # Compute forecasts for best model
    # bm = best model
    
    sarimax_bm = SARIMAX(endog,
                         exog = exog_full_train,
                         order = best_model.order,
                         trend = best_model.trend)
    sarimax_bm_res = sarimax_bm.fit()
    sarimax_bm_pred = sarimax_bm_res.get_prediction(exog = exog_pred,
                                    start = dt(endog.index[-1].year + 1, 12, 31), 
                                      end = dt(max_pred_year, 12, 31)).summary_frame()
    print(sarimax_bm_pred)
    
    
    if plot:
        sarimax_bm_pred['mean'].plot(c = 'b')
        endog_test.plot(c = 'g')
        sarimax_bm_pred['mean_ci_lower'].plot(c = 'r') 
        sarimax_bm_pred['mean_ci_upper'].plot(c = 'r');

    
    # Build final dictionary

    region_forecast = {
                        'region' : region_name,
                        'forecast' : sarimax_bm_pred,
                        'order' : best_model.order,
                        'trend' : best_model.trend,
                        'rmse' : min_rmse
                        }        
    print(region_forecast)
    
    return region_forecast    

#%% 

region = 'ΛΕΥΚΑΔΟΣ'

#endog = population_df[region]
#exog = full_deceases_df[region]
#exog.name = 'deceases'


#a = evaluate_forecasts(endog)

#%%
#sar = evaluate_forecasts_sarimax(endog, exog)
