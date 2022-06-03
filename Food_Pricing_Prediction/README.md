
# `Food Price Prediction Project`
## `objectives`
This project is aimed at forecasting or predicting the prices of various agricultural products found in all 36 states, and the federal capital territory, of Nigeria with reference to the prevailing exchange rates from US Dollars to Naira to help Nigerians in planning for the future.

## Project Setup
- Creation of a new folder tagged `Final_Project`.
- Creation of a virtual environment in the `Final_Project` folder.
```

python3 -m venv python_env
```

## Web_scraping
Installation of the required dependencies. 
```
pip install -r requirements.txt
```
- `Data`
This project uses the dataset from Nigeria's `National Bureau of Statistics'` tagged `Selected food price` from 2019 to 2021 - [Food_Price_Dataset](https://nigerianstat.gov.ng/resource/SELECTED%20FOOD%20(JAN_2019%20-%20NOV%202021).
Data showing the exchange rate from US Dollars to Naira for the corresponding years was also scraped from the `Exchangerates.org.uk` - [USD to Naira](https://www.exchangerates.org.uk USD-NGN-spot-exchange-rates-history-{year}.html).

## Data Preprocessing 
- `Data Cleaning`: Pandas is employed to clean the data. It includes transposing of the `Food Price Dataset` and merging the transposed dataset with the scraped `USD to Naira` exchange rates dataset.  

- `Data Visualization`: 

## Model Building 
- Best performing model: Random forest regression

## Future plans
- Model deployment

## Resources





