# -*- coding: utf-8 -*-
"""
Created on Tue May 10 13:45:22 2022

@author: Jaime García Chaparr
"""

#%% Import modules

import pandas as pd
from pandas.plotting import autocorrelation_plot
import numpy as np

from datetime import datetime as dt

from sklearn.metrics import mean_squared_error as mse

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA

from functions import evaluate_forecasts

#%% Import data

pop_filename = 'ypol_plith.xlsx'

df = pd.read_excel(f'../data/{pop_filename}', index_col = 'year',
                   parse_dates = True)

dfs = {
       'plith_raw' : df
       }

df = dfs['plith_raw'].copy()

#%% Cleaning 1

df = dfs['plith_raw'].copy()

#%% Analysis for nomos Evrou

evrou_raw = df['ΝΟΜΟΣ ΛΕΥΚΑΔΟΣ']

break_time = dt(2016, 1, 1)
e_train = evrou_raw[evrou_raw.index <= break_time]
e_test = evrou_raw[evrou_raw.index > break_time]

arima = ARIMA(e_train, order = (6, 0, 2)) #6, 0, 2
res = arima.fit()
print(res.summary())

e_pred = res.predict(start = dt(2017, 1, 1), end = dt(2021, 1, 1))

#e_test.plot(c = 'b'), 
#e_pred.plot(c = 'r');
print(mse(e_test, e_pred, squared = False))

#res.predict(start = dt(2017, 1, 1), end = dt(2021, 1, 1)).summary_frame()
e_pred_data = res.get_prediction(start = dt(2021, 1, 1), end = dt(2030, 1, 1)).summary_frame()
res.get_prediction(start = dt(2021, 1, 1), end = dt(2030, 1, 1)).summary_frame()
e_pred_data['mean'].plot(c = 'b')
e_test.plot(c = 'g')
e_pred_data['mean_ci_lower'].plot(c = 'r') 
e_pred_data['mean_ci_upper'].plot(c = 'r') 
#e_pred.plot(c = 'r');

#res.predict(e_test)
#AR = 5 order = 5, 1, 0
#res.predict(start = dt(2017, 1, 1), end = dt(2025, 1, 1))

#%% autocorr plot

autocorrelation_plot(evrou_raw)

#%% Test functions

reg = evaluate_forecasts(evrou_raw,
                         region_name = 'ΕΒΡΟΥ',
                         max_pred_year = 2030,
                         plot = True)


#%% Useful lines

res.get_forecast().conf_int()
res.get_forecast().predicted_mean
res.predict(start = dt(2017, 1, 1), end = dt(2025, 1, 1))
res.get_forecast().summary_frame()
res.get_forecast(steps = 5).summary_frame()
pd.concat(['a', res.forecast()], axis = 0)
res.get_prediction(start = dt(2017, 1, 1), end = dt(2025, 1, 1)).summary_frame()

e_pred_data = res.get_prediction(start = dt(2017, 1, 1), end = dt(2025, 1, 1)).summary_frame()
e_pred_data['mean'].plot(c = 'b')
e_pred_data['mean_ci_lower'].plot(c = 'r') 
e_pred_data['mean_ci_upper'].plot(c = 'r') 
