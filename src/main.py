# -*- coding: utf-8 -*-
"""
Created on Tue May 10 13:45:22 2022

@author: Jaime García Chaparr
"""

#%% Import modules

import pandas as pd
from pandas.plotting import autocorrelation_plot
import numpy as np

from datetime import datetime as dt

from sklearn.metrics import mean_squared_error as mse

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA

from functions import evaluate_forecasts

import warnings
warnings.filterwarnings("ignore")

#%% Import data

pop_filename = 'ypol_plith.xlsx'

df = pd.read_excel(f'../data/{pop_filename}', index_col = 'year',
                   parse_dates = True)

dfs = {
       'plith_raw' : df
       }

df = dfs['plith_raw'].copy()

#%% Cleaning 1

df = dfs['plith_raw'].copy()

df.columns = [col.replace('ΝΟΜΟΣ ', '').replace(' ', '_') for col in df.columns]
df.index = pd.date_range('2002', periods = len(df), freq = 'Y') #También 'AS-JAN'    
df.index.name = 'year'

#%% Save population.csv

df.to_csv('../data/processed_csv/population.csv')

#%% Load population.csv

df = pd.read_csv('../data/processed_csv/population.csv', index_col = 'year')

#%% Analysis for nomos Evrou SUCIOOOO

evrou_raw = df['ΚΕΡΚΥΡΑΣ']

break_time = dt(2016, 12, 31)
e_train = evrou_raw[evrou_raw.index <= break_time]
e_test = evrou_raw[evrou_raw.index > break_time]

arima = ARIMA(e_train, order = (2, 1, 2)) #6, 0, 2
res = arima.fit()
print(res.summary())

e_pred = res.predict(start = dt(2017, 1, 1), end = dt(2021, 1, 1))

#e_test.plot(c = 'b'), 
#e_pred.plot(c = 'r');
print(mse(e_test, e_pred, squared = False))

#res.predict(start = dt(2017, 1, 1), end = dt(2021, 1, 1)).summary_frame()
e_pred_data = res.get_prediction(start = dt(2017, 1, 1), end = dt(2021, 1, 1)).summary_frame()
res.get_prediction(start = dt(2021, 1, 1), end = dt(2030, 1, 1)).summary_frame()
e_pred_data['mean'].plot(c = 'b')
e_test.plot(c = 'g')
e_pred_data['mean_ci_lower'].plot(c = 'r') 
e_pred_data['mean_ci_upper'].plot(c = 'r') 
#e_pred.plot(c = 'r');

#res.predict(e_test)
#AR = 5 order = 5, 1, 0
#res.predict(start = dt(2017, 1, 1), end = dt(2025, 1, 1))

#%% autocorr plot

autocorrelation_plot(evrou_raw)

#%% Load deaths data

deaths = pd.read_csv('../data/processed_csv/deceases.csv', index_col = 'Unnamed: 0')

#%% Test functions

region = 'ΗΡΑΚΛΕΙΟΥ'

reg = evaluate_forecasts(df[region],
#                         exog = 
                         region_name = region,
                         max_pred_year = 2030,
                         plot = True)


#%% Compute models for all nomos

timeseries = {}

generate_forecasts = False

if generate_forecasts:
    for region in df.columns:
        ts = df[region]
        print(f'{region}')
        
        timeseries[region] = evaluate_forecasts(ts,
                                 region_name = region,
                                 max_pred_year = 2030,
                                 plot = True)
    
    predictions_df = pd.DataFrame(
                        data = {key : timeseries[key]['forecast']['mean'] 
                                for key in timeseries.keys()})
    predictions_df.index.name = 'year'
    
else:
    predictions_df = pd.read_csv('../data/processed_csv/forecasts.csv', 
                                 index_col = 'year')

full_timeseries_df = pd.concat([df, predictions_df], axis = 0)

#%% Save predictions

predictions_df.to_csv('../data/processed_csv/forecasts.csv')
full_timeseries_df.to_csv('../data/processed_csv/full_timeseries.csv')

#%% Load predictions

predictions_df = pd.read_csv('../data/processed_csv/forecasts.csv', index_col = 'year')
full_timeseries_df = pd.read_csv('../data/processed_csv/full_timeseries.csv', index_col = 'year')

#%% Save full timeseries to df

full_timeseries_df.to_excel('../data/final_data/full_timeseries.xlsx', 
                            sheet_name = 'timeseries')

#%% Load full timeseries to df

full_timeseries_df = pd.read_excel('../data/final_data/full_timeseries.xlsx', 
                            sheet_name = 'timeseries', index_col = 'year')
full_timeseries_df.index = full_timeseries_df.index.astype('datetime64[ns]')


#%% Unroll full timeseries

# Objetive: get a year, province, value structure

unrolled_df = pd.DataFrame(data = None)
for col in full_timeseries_df.columns:
    region_unroll = pd.DataFrame(data = {
                'year' : [i for i in range(2002, 2031)], 
                'nomos' : [col] * len(full_timeseries_df), 
                'population' : full_timeseries_df[col].tolist()
                })
    unrolled_df = pd.concat([unrolled_df, region_unroll], axis = 0)

unrolled_df.to_excel('../data/final_data/unrolled_timeseries.xlsx')
    
# =============================================================================
# pd.DataFrame(data = {
#             'year' : [i for i in range(2002, 2031)], 
#             'nomos' : ['ΕΒΡΟΥ'] * len(full_timeseries_df), 
#             'population' : full_timeseries_df['ΕΒΡΟΥ'].tolist()
#             })
# 
# =============================================================================

#%% Useful lines

res.get_forecast().conf_int()
res.get_forecast().predicted_mean
res.predict(start = dt(2017, 1, 1), end = dt(2025, 1, 1))
res.get_forecast().summary_frame()
res.get_forecast(steps = 5).summary_frame()
pd.concat(['a', res.forecast()], axis = 0)
res.get_prediction(start = dt(2017, 1, 1), end = dt(2025, 1, 1)).summary_frame()

e_pred_data = res.get_prediction(start = dt(2017, 1, 1), end = dt(2025, 1, 1)).summary_frame()
e_pred_data['mean'].plot(c = 'b')
e_pred_data['mean_ci_lower'].plot(c = 'r') 
e_pred_data['mean_ci_upper'].plot(c = 'r') 

