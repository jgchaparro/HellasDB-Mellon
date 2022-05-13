# -*- coding: utf-8 -*-
"""
Created on Thu May 12 13:13:23 2022

@author: Jaime García Chaparr
"""

import pandas as pd
import numpy as np
from functions import evaluate_forecasts_2

import pickle
import warnings
warnings.filterwarnings("ignore")

#%% Create forecasts for deaths

filename = 'deaths.xlsx'

def get_deceases_data(filename):
    """Extracts death data sheet by sheet"""
    
    # Initialize DF
    full_df = pd.DataFrame(data = None)
    
    years = [str(y) for y in range(2000, 2021)]

    for year in years:
        df_raw = pd.read_excel(f'../data/{filename}', sheet_name = year)
        year = int(year)
        
        df = df_raw.copy()
        
        # Preserve Attiki data
        if year > 2014:
            attiki_deaths = df.loc[61, 'Unnamed: 3']
            df = df.iloc[12:83, [2, 3]]
        else:
            attiki_deaths = df.loc[62, 'Unnamed: 3']
            df = df.iloc[12:79, [2, 3]]
        
        df.dropna(inplace = True)
        df.columns = ['nomos', year]
        
        # Clean nomos names
        df['nomos'] = df['nomos'].apply(lambda x: 
                                        x.replace('ΝΟΜΟΣ ', '').replace(' ', '_'))
        
        # Replace nomarchia data by attiki data
        if year > 2014:
            df = df[df['nomos'].str.contains('Π\.Ε.') == False]
        else:
            df = df[df['nomos'].str.contains('ΝΟΜΑΡΧΙΑ_') == False]
        
        
        df.set_index('nomos', inplace = True)
        df.loc['ΑΤΤΙΚΗ'] = attiki_deaths
        
        
        full_df = pd.concat([full_df, df.T], axis = 0)
    
    # Change index to date_range
    full_df.index = pd.date_range('2000', periods = len(full_df), freq = 'Y') #También 'AS-JAN'
    full_df = full_df.astype(int)
    
    return full_df

generate = False

if generate:
    deceases_df = get_deceases_data(filename)
    deceases_df.index.name = 'year'
    deceases_df.columns.name = None

#%% Save deceases_df

save = False

if save:
    deceases_df.to_csv('../data/processed_csv/deceases.csv')

#%% Load deceases_df

deceases_df = pd.read_csv('../data/processed_csv/deceases.csv', 
                          index_col = 'year')
deceases_df.index = deceases_df.index.astype('datetime64[ns]')
deceases_df.index.freq = 'Y'

#%% Generate timeseries

deceases_timeseries = {}

generate_forecasts = True

if generate_forecasts:
    for region in deceases_df.columns:
        ts = deceases_df[region]
        print(f'{region}')
        
        deceases_timeseries[region] = evaluate_forecasts_2(ts,
                                 region_name = region,
                                 max_pred_year = 2030,
                                 plot = True)
    
    deceases_pred_df = pd.DataFrame(
                        data = {key : deceases_timeseries[key]['forecast']['mean'] 
                                for key in deceases_timeseries.keys()})
    deceases_pred_df .index.name = 'year'
    
else:
    deceases_pred_df = pd.read_csv('../data/processed_csv/deceases_forecasts.csv', 
                                 index_col = 'year')

pickle.dump(deceases_timeseries, open('deceases_timeseries.p', "wb"))

full_deceases_timeseries_df = pd.concat([deceases_df, deceases_pred_df], axis = 0)

#%% Save predictions

deceases_pred_df.to_csv('../data/processed_csv/deceases_forecasts.csv')
full_deceases_timeseries_df.to_csv('../data/processed_csv/full_deceases_timeseries.csv')

#%% Load predictions

deceases_pred_df = pd.read_csv('../data/processed_csv/deceases_forecasts.csv', index_col = 'year')
deceases_pred_df.index = deceases_pred_df.index.astype('datetime64[ns]')
deceases_pred_df.index.freq = 'Y'

full_deceases_timeseries_df = pd.read_csv('../data/processed_csv/full_deceases_timeseries.csv', index_col = 'year')
full_deceases_timeseries_df .index = full_deceases_timeseries_df .index.astype('datetime64[ns]')
full_deceases_timeseries_df .index.freq = 'Y'

#%% Save full deceases timeseries to df

full_deceases_timeseries_df.to_excel('../data/final_data/full_timeseries_2.xlsx', 
                            sheet_name = 'deceases')


#%% Unroll timseries

# Objetive: get a year, province, value structure

unrolled_df = pd.DataFrame(data = None)
for col in deceases_timeseries.keys():
    deceases_data_unroll =  pd.DataFrame(data = {
                'year' : [i for i in range(2000, 2021)], 
                'nomos' : [col] * len(deceases_df), 
                'deceases' : deceases_df[col].tolist(),
                'deceases_ci_lower' : deceases_df[col].tolist(),
                'deceases_ci_upper' : deceases_df[col].tolist()})
                
    
    deceases_pred_unroll = pd.DataFrame(data = {
                'year' : [i for i in range(2021, 2031)], 
                'nomos' : [col] * len(deceases_pred_df), 
                'deceases' : deceases_timeseries[col]['forecast']['mean'],
                'deceases_ci_lower' : deceases_timeseries[col]['forecast']['mean_ci_lower'],
                'deceases_ci_upper' : deceases_timeseries[col]['forecast']['mean_ci_upper']})
    
    deceases_full_unroll = pd.concat([deceases_data_unroll, deceases_pred_unroll], axis = 0)
    unrolled_df = pd.concat([unrolled_df, deceases_full_unroll], axis = 0)
    unrolled_df.reset_index(drop = True, inplace = True)

unrolled_df.to_excel('../data/final_data/unrolled_deceases_timeseries.xlsx',
                     sheet_name = 'Deceases')
    