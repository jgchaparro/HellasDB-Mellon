# Hellas Mellon Project

![ithaki_banner](https://img.huffingtonpost.com/asset/5d83b9b63b0000c49fd79d32.jpeg?ops=1778_1000)

The Hellas Mellon Project aims to forecast the population and other metrics in Greece until 2030 based on data gathered from the Hellenic Statistical Service (ELSTAT).

To this end, 51 ARIMAX (autorregresive integrated moving average with exogenous regressors) models were computed for each of the 51 Greek regions according to NUTS 2 for the Attica and NUTS 3 for the rest of the country. An additional model for Ithaki was computed. The hyperparameters of each model were optimized through grid searching and rated according to their RMSE. The models with the lowest RMSE but inconsistent results were readjusted up to three times to correct unrealistic forecasts.

## Features

- Population data by region from 2002 to 2021 and forecasts up to 2030.
- Weddings, births, deaths and GDP per capita information from 2000 to 2020 and forecasts up to 2030.
- 95 % confidence intervals for all measures.

## Timeseries construction process

* Population forecast
    * Births
        * Weddings (lagged)
    * Deaths
    * Per capita GDP
        
The weddings forecast up to 2030 lagged one period was used to predict the trend in births. The births, deaths and per capita GDP were used as additional variables to compute the population timeseries forecast.


