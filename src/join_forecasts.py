# -*- coding: utf-8 -*-
"""
Created on Fri May 13 16:15:24 2022

@author: Jaime García Chaparr
"""

import pandas as pd
import numpy as np

#%% Load unrolled data

population_sarimax = pd.read_excel('../data/final_data/unrolled_population_sarimax_timeseries.xlsx')
births_sarimax = pd.read_excel('../data/final_data/unrolled_births_sarimax_timeseries.xlsx')
deceases = pd.read_excel('../data/final_data/unrolled_deceases_timeseries.xlsx')
weddings = pd.read_excel('../data/final_data/unrolled_weddings_timeseries.xlsx')
gdp = pd.read_excel('../data/final_data/unrolled_gdp_timeseries.xlsx')

dfs = [population_sarimax, births_sarimax, deceases, weddings, gdp]

for df in dfs:
    df.sort_values(by= ['nomos', 'year'], inplace = True)

#%% Create merged dataframe
    
merged_unrolled_df = population_sarimax.copy()

for df in dfs[1:]:
    merged_unrolled_df = pd.concat([merged_unrolled_df, df.iloc[:, -3:]], axis = 1)
    
#%% Save merged dataframe