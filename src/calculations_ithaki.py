# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:13:56 2022

@author: Jaime García Chaparr
"""

import pandas as pd
import numpy as np

#%% Import data 

df = pd.read_csv(r'C:\Users\jgcha\Desktop\IronHack\Semana 4\hellas_db\final_databases\hellas_db.csv')

# Get data for Kefallonia and Ithaki
df_kefith = df[df['nomos'].isin(['ΚΕΦΑΛΛΗΝΙΑΣ', 'ΙΘΑΚΗΣ'])]

# Group by nomos
grouped = df_kefith.groupby('nomos').sum()[['facto11', 'facto01', 'facto91']]

# Get percentage of population by census
perc_ith = grouped.loc['ΙΘΑΚΗΣ']/grouped.loc['ΚΕΦΑΛΛΗΝΙΑΣ']

# Create array with estimated population percentage of nomos' population
perc_91_01 = np.linspace(perc_ith['facto91'], perc_ith['facto01'], 10)
perc_01_11 = np.linspace(perc_ith['facto01'], perc_ith['facto11'], 10)

perc_array = np.concatenate([perc_91_01, perc_01_11])
perc_value = 0.084 # Itahi represents the 8,4% of the nomos population

#%% Apply proportions to predictions

full_timeseries = pd.read_excel('../data/final_data/full_timeseries.xlsx', 
                               sheet_name = 'full_database')

full_timeseries = full_timeseries.iloc[:, 1:]

# Get Kefallonia data
kef_ts = full_timeseries[full_timeseries['nomos'] == 'ΚΕΦΑΛΛΗΝΙΑΣ']
kef_values = kef_ts.iloc[:, 2:-3] # Exclude GDP per capita
ith_values = kef_ts.iloc[:, 2:-3] * 0.084

ith_ts = kef_ts.copy()
ith_ts.iloc[:, 2:-3] = ith_values
ith_ts['nomos'] = 'ΙΘΑΚΗΣ'

#%% Export Ithaki's data

ith_ts.to_excel('../data/final_data/ithaki_timeseries.xlsx',
                sheet_name = 'ithaki_timseries')
