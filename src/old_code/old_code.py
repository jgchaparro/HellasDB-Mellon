# -*- coding: utf-8 -*-
"""
Created on Sat May 14 13:04:13 2022

@author: Jaime García Chaparr
"""

#%% Correct timeseries

# =============================================================================
# exclude = {'ΙΩΑΝΝΙΝΩΝ' : [(2, 0, 1, 'c')]
#                 }
# 
# corrected_weddings_timeseries = {}
# 
# for region in exclude.keys():
#     ts = weddings_df[region]
#     print(f'{region}')
#     
#     corrected_weddings_timeseries[region] = correct_forecasts(ts[:-1],
#                                                             region_name = region,
#                                                             max_pred_year = 2030,
#                                                             plot = True,
#                                                             exclude = exclude,
#                                                             ps = [2],
#                                                             qs = [1]
#         )
#     
#     weddings_pred_df[region] = corrected_weddings_timeseries[region]['forecast']['mean']
# 
# 
