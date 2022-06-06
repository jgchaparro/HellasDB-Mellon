# -*- coding: utf-8 -*-
"""
Created on Fri May 13 12:35:32 2022

@author: Jaime García Chaparr
"""

import pandas as pd
import numpy as np
from functions import evaluate_forecasts_sarimax, correct_forecasts

import pickle
import warnings
warnings.filterwarnings("ignore")


#%% Load births_df

births_df = pd.read_csv('../data/processed_csv/births.csv', 
                          index_col = 'year')
births_df.index = births_df.index.astype('datetime64[ns]')
births_df.index.freq = 'Y'

#%% Load exogenous variables data

full_weddings_timeseries_df = pd.read_csv('../data/processed_csv/full_weddings_timeseries.csv', index_col = 'year')
full_weddings_timeseries_df.index = full_weddings_timeseries_df .index.astype('datetime64[ns]')
full_weddings_timeseries_df.index.freq = 'Y'

# Shift full_weddings_timeseries_df

lagged_full_weddings_timeseries_df = full_weddings_timeseries_df.shift(1)
lagged_full_weddings_timeseries_df.dropna(inplace = True)

#%% Generate timeseries

births_sarimax_timeseries = {}

generate_forecasts = True

if generate_forecasts:
    for region in births_df.columns:
        ts = births_df[region]
        print(f'{region}')
        
        births_sarimax_timeseries[region] = evaluate_forecasts_sarimax(ts,
                                 lagged_full_weddings_timeseries_df[region],                           
                                 region_name = region,
                                 start_year = 2001,
                                 max_pred_year = 2030,
                                 plot = True)
    
    births_sarimax_pred_df = pd.DataFrame(
                        data = {key : births_sarimax_timeseries[key]['forecast']['mean'] 
                                for key in births_sarimax_timeseries.keys()})
    births_sarimax_pred_df .index.name = 'year'
    
else:
    births_sarimax_pred_df = pd.read_csv('../data/processed_csv/births_sarimax_forecasts.csv', 
                                 index_col = 'year')

pickle.dump(births_sarimax_timeseries, open('births_sarimax_timeseries.p', "wb"))

#%% Correct predictions

correct_regions = ['ΙΩΑΝΝΙΝΩΝ', 'ΕΥΒΟΙΑΣ', 'ΛΕΣΒΟΥ', 'ΔΩΔΕΚΑΝΗΣΟΥ', 'ΠΡΕΒΕΖΗΣ',
                   'ΛΑΡΙΣΗΣ', 'ΚΥΚΛΑΔΩΝ', 'ΗΡΑΚΛΕΙΟΥ']

exclude = {key : [births_sarimax_timeseries[key]['order']]
           for key in correct_regions}
 
corrected_births_sarimax_timeseries = {}
 
for region in exclude.keys():
    ts = births_df[region]
    print(f'{region}')
     
    corrected_births_sarimax_timeseries[region] = correct_forecasts(ts,
                                                             region_name = region,
                                                             max_pred_year = 2030,
                                                             plot = True,
                                                             exclude = exclude
                                                             #ps = [3],
                                                             #ds = [0],
                                                             #qs = [3]
                                                             )

    births_sarimax_timeseries[region] = corrected_births_sarimax_timeseries[region]
     
    births_sarimax_pred_df[region] = corrected_births_sarimax_timeseries[region]['forecast']['mean'] 


#%% Second corrections

second_correct_regions = ['ΕΥΒΟΙΑΣ', 'ΔΩΔΕΚΑΝΗΣΟΥ', 'ΚΥΚΛΑΔΩΝ']

second_exclude = {key : [births_sarimax_timeseries[key]['order'],
                         corrected_births_sarimax_timeseries[key]['order']]
           for key in second_correct_regions}

second_corrected_births_sarimax_timeseries = {}
 
for region in second_exclude.keys():
    ts = births_df[region]
    print(f'{region}')
     
    second_corrected_births_sarimax_timeseries[region] = correct_forecasts(ts,
                                                             region_name = region,
                                                             max_pred_year = 2030,
                                                             plot = True,
                                                             exclude = exclude,
                                                             ps = [1, 2, 3],
                                                             ds = [0],
                                                             qs = [1]
                                                             )
    
    births_sarimax_timeseries[region] = second_corrected_births_sarimax_timeseries[region]
    
    births_sarimax_pred_df[region] = second_corrected_births_sarimax_timeseries[region]['forecast']['mean']

full_births_sarimax_timeseries_df = pd.concat([births_df, births_sarimax_pred_df], axis = 0)

#%% Save predictions

births_sarimax_pred_df.to_csv('../data/processed_csv/births_sarimax_forecasts.csv')
full_births_sarimax_timeseries_df.to_csv('../data/processed_csv/full_births_sarimax_timeseries.csv')

#%% Load predictions

births_sarimax_pred_df = pd.read_csv('../data/processed_csv/births_sarimax_forecasts.csv', index_col = 'year')
births_sarimax_pred_df.index = births_sarimax_pred_df.index.astype('datetime64[ns]')
births_sarimax_pred_df.index.freq = 'Y'

full_births_sarimax_timeseries_df = pd.read_csv('../data/processed_csv/full_births_sarimax_timeseries.csv', index_col = 'year')
full_births_sarimax_timeseries_df .index = full_births_sarimax_timeseries_df .index.astype('datetime64[ns]')
full_births_sarimax_timeseries_df .index.freq = 'Y'

#%% Save full births_sarimax timeseries to df

full_births_sarimax_timeseries_df.to_excel('../data/final_data/full_timeseries_2.xlsx', 
                            sheet_name = 'births_sarimax')

#%% Unroll timseries

# Objetive: get a year, province, value structure

unrolled_df = pd.DataFrame(data = None)
for col in births_sarimax_timeseries.keys():
    births_sarimax_data_unroll =  pd.DataFrame(data = {
                'year' : [i for i in range(2000, 2021)], 
                'nomos' : [col] * len(births_df), 
                'births' : births_df[col].tolist(),
                'births_sarimax_ci_lower' : births_df[col].tolist(),
                'births_sarimax_ci_upper' : births_df[col].tolist()})
                
    
    births_sarimax_pred_unroll = pd.DataFrame(data = {
                'year' : [i for i in range(2021, 2031)], 
                'nomos' : [col] * len(births_sarimax_pred_df), 
                'births' : births_sarimax_timeseries[col]['forecast']['mean'],
                'births_sarimax_ci_lower' : births_sarimax_timeseries[col]['forecast']['mean_ci_lower'],
                'births_sarimax_ci_upper' : births_sarimax_timeseries[col]['forecast']['mean_ci_upper']})
    
    births_sarimax_full_unroll = pd.concat([births_sarimax_data_unroll, births_sarimax_pred_unroll], axis = 0)
    unrolled_df = pd.concat([unrolled_df, births_sarimax_full_unroll], axis = 0)
    unrolled_df.reset_index(drop = True, inplace = True)

unrolled_df.to_excel('../data/final_data/unrolled_births_sarimax_timeseries.xlsx',
                     sheet_name = 'births')

unrolled_df.to_excel('../data/final_data/integrated_timeseries.xlsx',
                     sheet_name = 'births')


