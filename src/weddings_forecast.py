# -*- coding: utf-8 -*-
"""
Created on Thu May 12 15:42:58 2022

@author: Jaime García Chaparr
"""

import pandas as pd
import numpy as np
from functions import evaluate_forecasts_2

import warnings
warnings.filterwarnings("ignore")

#%% Import data

filename = 'weddings.xlsx'

weddings_df = pd.read_excel(f'../data/{filename}', sheet_name = 'table_trans', 
                            index_col = 'year')
weddings_df.index = pd.date_range('2000', periods = len(weddings_df), freq = 'Y') #También 'AS-JAN'    
weddings_df.index.name = 'year'

#%% Generate timeseries

weddings_timeseries = {}

generate_forecasts = True

if generate_forecasts:
    for region in weddings_df.columns:
        ts = weddings_df[region]
        print(f'{region}')
        
        weddings_timeseries[region] = evaluate_forecasts_2(ts,
                                 region_name = region,
                                 max_pred_year = 2030,
                                 plot = True)
    
    weddings_pred_df = pd.DataFrame(
                        data = {key : weddings_timeseries[key]['forecast']['mean'] 
                                for key in weddings_timeseries.keys()})
    weddings_pred_df .index.name = 'year'
    
else:
    weddings_pred_df = pd.read_csv('../data/processed_csv/weddings_forecasts.csv', 
                                 index_col = 'year')

full_weddings_timeseries_df = pd.concat([weddings_df, weddings_pred_df], axis = 0)

#%% Save predictions

weddings_pred_df.to_csv('../data/processed_csv/weddings_forecasts.csv')
full_weddings_timeseries_df.to_csv('../data/processed_csv/full_weddings_timeseries.csv')

#%% Load predictions

weddings_pred_df = pd.read_csv('../data/processed_csv/weddings_forecasts.csv', index_col = 'year')
weddings_pred_df.index = weddings_pred_df.index.astype('datetime64[ns]')
weddings_pred_df.index.freq = 'Y'

full_weddings_timeseries_df = pd.read_csv('../data/processed_csv/full_weddings_timeseries.csv', index_col = 'year')
full_weddings_timeseries_df .index = full_weddings_timeseries_df .index.astype('datetime64[ns]')
full_weddings_timeseries_df .index.freq = 'Y'

#%% Save full weddings timeseries to df

full_weddings_timeseries_df.to_excel('../data/final_data/full_timeseries_2.xlsx', 
                            sheet_name = 'weddings')

#%% Unroll timseries

# Objetive: get a year, province, value structure

unrolled_df = pd.DataFrame(data = None)
for col in weddings_timeseries.keys():
    weddings_data_unroll =  pd.DataFrame(data = {
                'year' : [i for i in range(2000, 2021)], 
                'nomos' : [col] * len(weddings_df), 
                'weddings' : weddings_df[col].tolist(),
                'weddings_ci_lower' : weddings_df[col].tolist(),
                'weddings_ci_upper' : weddings_df[col].tolist()})
                
    
    weddings_pred_unroll = pd.DataFrame(data = {
                'year' : [i for i in range(2021, 2031)], 
                'nomos' : [col] * len(weddings_pred_df), 
                'weddings' : weddings_timeseries[col]['forecast']['mean'],
                'weddings_ci_lower' : weddings_timeseries[col]['forecast']['mean_ci_lower'],
                'weddings_ci_upper' : weddings_timeseries[col]['forecast']['mean_ci_upper']})
    
    weddings_full_unroll = pd.concat([weddings_data_unroll, weddings_pred_unroll], axis = 0)
    unrolled_df = pd.concat([unrolled_df, weddings_full_unroll], axis = 0)
    unrolled_df.reset_index(drop = True, inplace = True)


unrolled_df.to_excel('../data/final_data/unrolled_weddings_timeseries.xlsx',
                     sheet_name = 'weddings')

unrolled_df.to_excel('../data/final_data/integrated_timeseries.xlsx',
                     sheet_name = 'weddings')


