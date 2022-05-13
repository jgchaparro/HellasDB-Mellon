# -*- coding: utf-8 -*-
"""
Created on Fri May 13 15:28:09 2022

@author: Jaime García Chaparr
"""

import pandas as pd
import numpy as np
from functions import evaluate_forecasts_sarimax

import pickle
import warnings
warnings.filterwarnings("ignore")


#%% Load population_df

population_df = pd.read_csv('../data/processed_csv/population.csv', 
                          index_col = 'year')
population_df.index = population_df.index.astype('datetime64[ns]')
population_df.index.freq = 'Y'

#%% Load exogenous variables data

# =============================================================================
# full_weddings_timeseries_df = pd.read_csv('../data/processed_csv/full_weddings_timeseries.csv', index_col = 'year')
# full_weddings_timeseries_df.index = full_weddings_timeseries_df .index.astype('datetime64[ns]')
# full_weddings_timeseries_df.index.freq = 'Y'
# 
# =============================================================================

full_births_sarimax_timeseries_df = pd.read_csv('../data/processed_csv/full_births_sarimax_timeseries.csv', index_col = 'year')
full_births_sarimax_timeseries_df .index = full_births_sarimax_timeseries_df .index.astype('datetime64[ns]')
full_births_sarimax_timeseries_df .index.freq = 'Y'

full_deceases_timeseries_df = pd.read_csv('../data/processed_csv/full_deceases_timeseries.csv', index_col = 'year')
full_deceases_timeseries_df .index = full_deceases_timeseries_df .index.astype('datetime64[ns]')
full_deceases_timeseries_df .index.freq = 'Y'

full_gdp_timeseries_df = pd.read_csv('../data/processed_csv/full_gdp_timeseries.csv', index_col = 'year')
full_gdp_timeseries_df .index = full_gdp_timeseries_df .index.astype('datetime64[ns]')
full_gdp_timeseries_df .index.freq = 'Y'

#%% Merge all exogenous variables into one exogenous matrix

exog_data = [full_births_sarimax_timeseries_df, 
             full_deceases_timeseries_df,
             full_gdp_timeseries_df]
exog_matrix = {}

for region in population_df.columns:
    # Create dataframe with three exogenous variables per region
    exog_region_df = pd.concat([full_births_sarimax_timeseries_df[region], 
                                full_deceases_timeseries_df[region],
                                full_gdp_timeseries_df[region]], 
                               axis = 1)
    exog_region_df.columns = ['births_sarimax', 'deaths', 'gdp']
    exog_matrix[region] = exog_region_df
        
#%% Save exogenous variables matrix

pickle.dump(exog_matrix, open('exog_matrix.p', "wb"))

#%% Generate timeseries

population_sarimax_timeseries = {}

generate_forecasts = True

if generate_forecasts:
    for region in population_df.columns:
        ts = population_df[region]
        print(f'{region}')
        
        population_sarimax_timeseries[region] = evaluate_forecasts_sarimax(ts,
                                 exog_matrix[region],                           
                                 region_name = region,
                                 start_year = 2002,
                                 max_pred_year = 2030,
                                 plot = True)
    
    population_sarimax_pred_df = pd.DataFrame(
                        data = {key : population_sarimax_timeseries[key]['forecast']['mean'] 
                                for key in population_sarimax_timeseries.keys()})
    population_sarimax_pred_df .index.name = 'year'
    
else:
    population_sarimax_pred_df = pd.read_csv('../data/processed_csv/population_sarimax_forecasts.csv', 
                                 index_col = 'year')

pickle.dump(population_sarimax_timeseries, open('population_sarimax_timeseries.p', "wb"))

full_population_sarimax_timeseries_df = pd.concat([population_df, population_sarimax_pred_df], axis = 0)

#%% Save predictions

population_sarimax_pred_df.to_csv('../data/processed_csv/population_sarimax_forecasts.csv')
full_population_sarimax_timeseries_df.to_csv('../data/processed_csv/full_population_sarimax_timeseries.csv')

#%% Load predictions

population_sarimax_pred_df = pd.read_csv('../data/processed_csv/population_sarimax_forecasts.csv', index_col = 'year')
population_sarimax_pred_df.index = population_sarimax_pred_df.index.astype('datetime64[ns]')
population_sarimax_pred_df.index.freq = 'Y'

full_population_sarimax_timeseries_df = pd.read_csv('../data/processed_csv/full_population_sarimax_timeseries.csv', index_col = 'year')
full_population_sarimax_timeseries_df .index = full_population_sarimax_timeseries_df .index.astype('datetime64[ns]')
full_population_sarimax_timeseries_df .index.freq = 'Y'

#%% Save full population_sarimax timeseries to df

full_population_sarimax_timeseries_df.to_excel('../data/final_data/full_timeseries_2.xlsx', 
                            sheet_name = 'population_sarimax')

#%% Unroll timseries

# Objetive: get a year, province, value structure

unrolled_df = pd.DataFrame(data = None)
for col in population_sarimax_timeseries.keys():
    population_sarimax_data_unroll =  pd.DataFrame(data = {
                'year' : [i for i in range(2002, 2022)], 
                'nomos' : [col] * len(population_df), 
                'population_sarimax' : population_df[col].tolist(),
                'population_sarimax_ci_lower' : population_df[col].tolist(),
                'population_sarimax_ci_upper' : population_df[col].tolist()})
                
    
    population_sarimax_pred_unroll = pd.DataFrame(data = {
                'year' : [i for i in range(2022, 2031)], 
                'nomos' : [col] * len(population_sarimax_pred_df), 
                'population_sarimax' : population_sarimax_timeseries[col]['forecast']['mean'],
                'population_sarimax_ci_lower' : population_sarimax_timeseries[col]['forecast']['mean_ci_lower'],
                'population_sarimax_ci_upper' : population_sarimax_timeseries[col]['forecast']['mean_ci_upper']})
    
    population_sarimax_full_unroll = pd.concat([population_sarimax_data_unroll, population_sarimax_pred_unroll], axis = 0)
    unrolled_df = pd.concat([unrolled_df, population_sarimax_full_unroll], axis = 0)
    unrolled_df.reset_index(drop = True, inplace = True)

unrolled_df.to_excel('../data/final_data/unrolled_population_sarimax_timeseries.xlsx',
                     sheet_name = 'population_sarimax')
    