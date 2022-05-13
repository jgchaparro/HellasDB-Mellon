# -*- coding: utf-8 -*-
"""
Created on Fri May 13 12:07:30 2022

@author: Jaime García Chaparr
"""

import pandas as pd
import numpy as np

from functions import evaluate_forecasts_2
from utils import order

import pickle
import warnings
warnings.filterwarnings("ignore")

#%% Import data

filename = 'GDP per capita.xlsx'

gdp_df = pd.read_excel(f'../data/{filename}', sheet_name = 'transp_table', 
                            index_col = 'year')
gdp_df.index = pd.date_range('2000', periods = len(gdp_df), freq = 'Y') #También 'AS-JAN'    
gdp_df.index.name = 'year'

# Reorder columns 
gdp_df = gdp_df[order]

#%% Generate timeseries

gdp_timeseries = {}

generate_forecasts = True

if generate_forecasts:
    for region in gdp_df.columns:
        ts = gdp_df[region]
        print(f'{region}')
        
        gdp_timeseries[region] = evaluate_forecasts_2(ts,
                                 region_name = region,
                                 max_pred_year = 2030,
                                 trends = [None, 't'],
                                 plot = True)
    
    gdp_pred_df = pd.DataFrame(
                        data = {key : gdp_timeseries[key]['forecast']['mean'] 
                                for key in gdp_timeseries.keys()})
    gdp_pred_df.index.name = 'year'
    
else:
    gdp_pred_df = pd.read_csv('../data/processed_csv/gdp_forecasts.csv', 
                                 index_col = 'year')

pickle.dump(gdp_timeseries, open('gdp_timeseries.p', "wb"))

full_gdp_timeseries_df = pd.concat([gdp_df, gdp_pred_df], axis = 0)

#%% Save predictions

gdp_pred_df.to_csv('../data/processed_csv/gdp_forecasts.csv')
full_gdp_timeseries_df.to_csv('../data/processed_csv/full_gdp_timeseries.csv')

#%% Load predictions

gdp_pred_df = pd.read_csv('../data/processed_csv/gdp_forecasts.csv', index_col = 'year')
gdp_pred_df.index = gdp_pred_df.index.astype('datetime64[ns]')
gdp_pred_df.index.freq = 'Y'

full_gdp_timeseries_df = pd.read_csv('../data/processed_csv/full_gdp_timeseries.csv', index_col = 'year')
full_gdp_timeseries_df .index = full_gdp_timeseries_df .index.astype('datetime64[ns]')
full_gdp_timeseries_df .index.freq = 'Y'

#%% Save full gdp timeseries to df

full_gdp_timeseries_df.to_excel('../data/final_data/full_timeseries_2.xlsx', 
                            sheet_name = 'gdp')

#%% Unroll timseries

# Objetive: get a year, province, value structure

unrolled_df = pd.DataFrame(data = None)
for col in gdp_timeseries.keys():
    gdp_data_unroll =  pd.DataFrame(data = {
                'year' : [i for i in range(2000, 2020)], 
                'nomos' : [col] * len(gdp_df), 
                'gdp' : gdp_df[col].tolist(),
                'gdp_ci_lower' : gdp_df[col].tolist(),
                'gdp_ci_upper' : gdp_df[col].tolist()})
                
    
    gdp_pred_unroll = pd.DataFrame(data = {
                'year' : [i for i in range(2020, 2031)], 
                'nomos' : [col] * len(gdp_pred_df), 
                'gdp' : gdp_timeseries[col]['forecast']['mean'],
                'gdp_ci_lower' : gdp_timeseries[col]['forecast']['mean_ci_lower'],
                'gdp_ci_upper' : gdp_timeseries[col]['forecast']['mean_ci_upper']})
    
    gdp_full_unroll = pd.concat([gdp_data_unroll, gdp_pred_unroll], axis = 0)
    unrolled_df = pd.concat([unrolled_df, gdp_full_unroll], axis = 0)
    unrolled_df.reset_index(drop = True, inplace = True)

# Correct for negatives
#unrolled_df[unrolled_df < 0]

unrolled_df.to_excel('../data/final_data/unrolled_gdp_timeseries.xlsx',
                     sheet_name = 'gdp')

unrolled_df.to_excel('../data/final_data/integrated_timeseries_2.xlsx',
                     sheet_name = 'gdp')
