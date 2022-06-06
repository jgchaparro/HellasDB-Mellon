# -*- coding: utf-8 -*-
"""
Created on Thu May 12 12:11:29 2022

@author: Jaime García Chaparr
"""

import pandas as pd
from pandas.plotting import autocorrelation_plot
import numpy as np

from datetime import datetime as dt

from sklearn.metrics import mean_squared_error as mse

from statsmodels.tsa.arima.model import ARIMA

from functions import evaluate_forecasts_2

import warnings
warnings.filterwarnings("ignore")

import pickle

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

# Remove dots from Achaea
df.rename(columns = {'ΑΧΑΪΑΣ' : 'ΑΧΑΙΑΣ'}, inplace = True)


#%% Save population.csv

df.to_csv('../data/processed_csv/population.csv')

#%% Load population.csv

df = pd.read_csv('../data/processed_csv/population.csv', index_col = 'year')
df.index = df.index.astype('datetime64[ns]')
df.index.freq = 'Y'

#%% Compute models for all nomos

timeseries = {}

generate_forecasts = True

if generate_forecasts:
    for region in df.columns:
        ts = df[region]
        print(f'{region}')
        
        timeseries[region] = evaluate_forecasts_2(ts,
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

#pickle.dump(timeseries, open('full_timeseries.p', "wb"))

full_timeseries_df = pd.concat([df, predictions_df], axis = 0)

#%% Save predictions

predictions_df.to_csv('../data/processed_csv/forecasts.csv')
full_timeseries_df.to_csv('../data/processed_csv/full_timeseries.csv')

#%% Load predictions

predictions_df = pd.read_csv('../data/processed_csv/forecasts.csv', index_col = 'year')
predictions_df.index = predictions_df.index.astype('datetime64[ns]')
predictions_df.index.freq = 'Y'

full_timeseries_df = pd.read_csv('../data/processed_csv/full_timeseries.csv', index_col = 'year')
full_timeseries_df .index = full_timeseries_df .index.astype('datetime64[ns]')
full_timeseries_df .index.freq = 'Y'

#%% Save full timeseries to df

full_timeseries_df.to_excel('../data/final_data/full_timeseries.xlsx', 
                            sheet_name = 'timeseries')

#%% Unroll timseries

# Objetive: get a year, province, value structure

unrolled_df = pd.DataFrame(data = None)
for col in timeseries.keys():
    region_data_unroll =  pd.DataFrame(data = {
                'year' : [i for i in range(2002, 2022)], 
                'nomos' : [col] * len(df), 
                'population' : df[col].tolist(),
                'ci_lower' : df[col].tolist(),
                'ci_upper' : df[col].tolist()})
                
    
    region_pred_unroll = pd.DataFrame(data = {
                'year' : [i for i in range(2022, 2031)], 
                'nomos' : [col] * len(predictions_df), 
                'population' : timeseries[col]['forecast']['mean'],
                'ci_lower' : timeseries[col]['forecast']['mean_ci_lower'],
                'ci_upper' : timeseries[col]['forecast']['mean_ci_upper']})
    
    region_full_unroll = pd.concat([region_data_unroll, region_pred_unroll], axis = 0)
    unrolled_df = pd.concat([unrolled_df, region_full_unroll], axis = 0)
    unrolled_df.reset_index(drop = True, inplace = True)

unrolled_df.to_excel('../data/final_data/unrolled_timeseries.xlsx',
                     sheet_name = 'Population')
    