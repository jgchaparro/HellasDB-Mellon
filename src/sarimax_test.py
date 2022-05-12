# -*- coding: utf-8 -*-
"""
Created on Thu May 12 10:24:35 2022

@author: Jaime García Chaparr
"""

import pandas as pd


#%% Import data

population_df = pd.read_csv('../data/processed_csv/population.csv', index_col = 'year') 
population_df.index = population_df.index.astype('datetime64[ns]')
population_df.index.freq = 'Y'


full_deceases_df = pd.read_csv('../data/processed_csv/deceases.csv', 
                          index_col = 'year')
full_deceases_df.index = full_deceases_df.index.astype('datetime64[ns]')
full_deceases_df.index.freq = 'Y'


