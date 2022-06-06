# Hellas Mellon Project

![ithaki_banner](https://img.huffingtonpost.com/asset/5d83b9b63b0000c49fd79d32.jpeg?ops=1778_1000)

The Hellas Mellon Project aims to forecast the population and other metrics in Greece until 2030 based on data gathered from the Hellenic Statistical Service (ELSTAT).

To this end, 51 ARIMAX (autorregresive integrated moving average with exogenous regressors) models were computed for each of the 51 Greek regions according to NUTS 2 for the Attica and NUTS 3 for the rest of the country. An additional model for Ithaki was computed. The hyperparameters of each model were optimized through grid searching and rated according to their RMSE. The models with the lowest RMSE but inconsistent results were readjusted up to three times to correct unrealistic forecasts.

## Features

- Population data by region from 2002 to 202 and forecasts up to 2030.
- Weddings, births, deaths and GDP per capita information from 2000 to 2020 and forecasts up to 2030.
- 95 % confidence intervals for all measures.
- A separated forecast for Ithaki using approximate measures.
- [A dashboard in Tableau for the interactive visualization of forecasts](https://public.tableau.com/app/profile/jgchaparro/viz/HellasMellonDashboard/HellasMellonDashboard).

## Timeseries construction process

* Population forecast
    * Births
        * Weddings (lagged)
    * Deaths
    * Per capita GDP
        
The weddings forecast up to 2030 lagged one period was used to predict the trend in births. The births, deaths and per capita GDP were used as additional variables to compute the population timeseries forecast.

## Sources

- [ELSTAT](https://www.statistics.gr/el/home/)

## Main files

- `results/timeseries_forecasts.csv`: historical data and forecasts for all measures.
- `results/timeseries_forecasts.xlsx`: same data as an Excel spreadsheet. Includes a table with coordinates indicating the center for each province for visualization purposes.

## Steps taken

1. Downloading files with regional timeseries for various measures form ELSTAT: estimated population, weddings, births, deaths and GDP per capita.
1. Creating auxiliary forecasts for `weddings`.
1. Computing ARIMAX models for `births` with `weddings` as an exogenous variable.
1. Creating auxiliary forecasts with ARIMA models for `GDP per capita` and `deaths`.
1. Modelizing future population for each region with ARIMA models with `births`, `deaths` and `GDP per capita` as additional variables to improve predictions.
1. Separating and generating a separate model for Ithaki.
1. Generating an [interactive dashboard in Tableau](https://public.tableau.com/app/profile/jgchaparro/viz/HellasMellonDashboard/HellasMellonDashboard?publish=yes).

## Next steps

- Convert location names in Katharevousa Greek to Dimotiki Greek.
- Find coordinates for the last remaing 300 units without data.  
- Separate the capital columns (`edres_`) to form a new table.
- Generate a version using Latin characters instead of Greek letters to improve accesibility for non-Greek-speaking users.

## Technology Stack

The following libraries were used in this project:

![Pandas](https://img.shields.io/badge/Pandas-1.3.4-blue)
![Numpy](https://img.shields.io/badge/NumPy-1.21.4-white)
![StatsModels](https://img.shields.io/badge/StatsModels-2.26-blue)

