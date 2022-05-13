# -*- coding: utf-8 -*-
"""
Created on Thu May 12 13:26:50 2022

@author: Jaime García Chaparr
"""

import pandas as pd
import numpy as np
from functions import evaluate_forecasts_2



import warnings
warnings.filterwarnings("ignore")

#%% Get births data

filename = 'births_mod.xlsx'

def get_births_data(filename):
    """Extracts death data sheet by sheet"""

    # Initialize DF
    full_df = pd.DataFrame(data = None)
    
    years = [str(y) for y in range(2000, 2021)]

    for year in years:
        df_raw = pd.read_excel(f'../data/{filename}', sheet_name = year)
        year = int(year)
        
        df = df_raw.copy()        
        df = df.iloc[34:, :2]
        df.columns = ['nomos', 'births']
        
        # Retain Attiki information
        attiki_births = df[df['nomos' ] == 'ΑΤΤΙΚΗ']['births'].iloc[0]
        
        # Drop all non-nomos columns and rename
        df = df[df['nomos'].str.contains('ΝΟΜ')]
        df['nomos'] = df['nomos'].apply(lambda x: 
                                        x.replace('ΝΟΜΟΣ ', '').replace(' ', '_'))
            
        # Add Attiki data
        df.set_index('nomos', inplace = True)
        df.loc['ΑΤΤΙΚΗ'] = attiki_births
        

        full_df = pd.concat([full_df, df.T], axis = 0)
    
    # Modify final df
    full_df.index = pd.date_range('2000', periods = len(full_df), freq = 'Y') #También 'AS-JAN'
    full_df = full_df.astype(int)
    full_df.index.name = 'year'
    full_df.columns.name = None

    

    return full_df

generate = False

if generate:
    births_df = get_births_data(filename)

#%% Save births_df

save = False

if save:
    births_df.to_csv('../data/processed_csv/births.csv')

#%% Load births_df

births_df = pd.read_csv('../data/processed_csv/births.csv', 
                          index_col = 'year')
births_df.index = births_df.index.astype('datetime64[ns]')
births_df.index.freq = 'Y'


#%% Generate timeseries

births_timeseries = {}

generate_forecasts = True

if generate_forecasts:
    for region in births_df.columns:
        ts = births_df[region]
        print(f'{region}')
        
        births_timeseries[region] = evaluate_forecasts_2(ts,
                                 region_name = region,
                                 max_pred_year = 2030,
                                 plot = True)
    
    births_pred_df = pd.DataFrame(
                        data = {key : births_timeseries[key]['forecast']['mean'] 
                                for key in births_timeseries.keys()})
    births_pred_df .index.name = 'year'
    
else:
    births_pred_df = pd.read_csv('../data/processed_csv/births_forecasts.csv', 
                                 index_col = 'year')

full_births_timeseries_df = pd.concat([births_df, births_pred_df], axis = 0)



#%% Unroll timseries

# Objetive: get a year, province, value structure

unrolled_df = pd.DataFrame(data = None)
for col in births_timeseries.keys():
    births_data_unroll =  pd.DataFrame(data = {
                'year' : [i for i in range(2000, 2021)], 
                'nomos' : [col] * len(births_df), 
                'births' : births_df[col].tolist(),
                'births_ci_lower' : births_df[col].tolist(),
                'births_ci_upper' : births_df[col].tolist()})
                
    
    births_pred_unroll = pd.DataFrame(data = {
                'year' : [i for i in range(2021, 2031)], 
                'nomos' : [col] * len(births_pred_df), 
                'births' : births_timeseries[col]['forecast']['mean'],
                'births_ci_lower' : births_timeseries[col]['forecast']['mean_ci_lower'],
                'births_ci_upper' : births_timeseries[col]['forecast']['mean_ci_upper']})
    
    births_full_unroll = pd.concat([births_data_unroll, births_pred_unroll], axis = 0)
    unrolled_df = pd.concat([unrolled_df, births_full_unroll], axis = 0)
    unrolled_df.reset_index(drop = True, inplace = True)

unrolled_df.to_excel('../data/final_data/unrolled_births_timeseries.xlsx',
                     sheet_name = 'births')

unrolled_df.to_excel('../data/final_data/integrated_timeseries.xlsx',
                     sheet_name = 'births')
