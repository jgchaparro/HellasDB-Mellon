# -*- coding: utf-8 -*-
"""
Created on Fri May 13 16:15:24 2022

@author: Jaime García Chaparr
"""

import pandas as pd
import numpy as np

#%% Load unrolled data

population_sarimax = pd.read_excel('../data/final_data/unrolled_population_sarimax_timeseries.xlsx', 
                                   
                                   index_col = 'year')
births_sarimax = pd.read_excel('../data/final_data/unrolled_births_sarimax_timeseries.xlsx', 
                                   index_col = 'year')
deceases = pd.read_excel('../data/final_data/unrolled_deceases_timeseries.xlsx', 
                                   index_col = 'year')
weddings = pd.read_excel('../data/final_data/unrolled_weddings_timeseries.xlsx', 
                                   index_col = 'year')
gdp = pd.read_excel('../data/final_data/unrolled_gdp_timeseries.xlsx', 
                                   index_col = 'year')

dfs = [population_sarimax, births_sarimax, deceases, weddings, gdp]
dfs_mod = []

for df in dfs:
    df.sort_values(by = ['nomos', 'year'], inplace = True)
    df = df[df.index >= 2002]
    dfs_mod.append(df)


#%% Create merged dataframe
    
merged_unrolled_df = population_sarimax.copy()

for df in dfs_mod[1:]:
    merged_unrolled_df = pd.concat([merged_unrolled_df, df.iloc[:, -3:]], axis = 1)

merged_unrolled_df.reset_index(inplace = True)
merged_unrolled_df.drop(columns = 'Unnamed: 0', inplace = True)

#%% Save merged dataframe

merged_unrolled_df.to_excel('../data/final_data/full_timeseries.xlsx',
                     sheet_name = 'full_database')