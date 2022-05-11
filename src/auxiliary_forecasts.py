# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:35:01 2022

@author: Jaime García Chaparr
"""

#%% Import modules

import pandas as pd
import numpy as np
from functions import evaluate_forecasts

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

deceases_df = get_deceases_data(filename)

#%% Save deceases_df

deceases_df.to_csv('../data/processed_csv/deceases.csv')

#%% Extend timeseries until 2030

region = 'ΗΡΑΚΛΕΙΟΥ'

reg = evaluate_forecasts(deceases_df[region],
                         region_name = region,
                         max_pred_year = 2030,
                         plot = True)

