# -*- coding: utf-8 -*-
"""
Created on Thu May 12 10:24:35 2022

@author: Jaime García Chaparr
"""

import pandas as pd
from datetime import datetime as dt

import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error as mse

import warnings
warnings.filterwarnings("ignore")



#%% Import data

population_df = pd.read_csv('../data/processed_csv/population.csv', index_col = 'year') 
population_df.index = population_df.index.astype('datetime64[ns]')
population_df.index.freq = 'Y'


full_deceases_df = pd.read_csv('../data/processed_csv/deceases_full_timeseries.csv', 
                          index_col = 'year')
full_deceases_df.index = full_deceases_df.index.astype('datetime64[ns]')
full_deceases_df.index.freq = 'Y'

deceases_df = full_deceases_df[(full_deceases_df.index > dt(2001, 12, 31)) & 
                               (full_deceases_df.index < dt(2022, 12, 31))]

#%% Test region

region = 'ΛΕΥΚΑΔΟΣ'

endog = population_df[region]
exog = deceases_df[region]
exog.name = 'deceases'

#exog = sm.add_constant(exog)

exog.columns = ['const', 'deaths']

break_time = dt(2016, 12, 31)
endog_train = endog[endog.index <= break_time]
endog_test= endog[endog.index > break_time]

exog_train = exog[exog.index <= break_time]
exog_test= exog[exog.index > break_time]

sarimax = SARIMAX(endog_train, 
                  exog = exog_train,
                  order = (2, 1, 2)) #6, 0, 2
res = sarimax.fit()
print(res.summary())

endog_pred = res.predict(
                            exog = exog_test,
                         start = dt(2017, 1, 1), 
                         end = dt(2021, 1, 1))


print(mse(endog_test, endog_pred, squared = False))

