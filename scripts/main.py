import os
from helpers import download_data, get_directory_path
from alpha3 import get_alpha3
from ccse_data_to_json import ccse_data_to_json

json_dir, csv_dir, data_dir = get_directory_path("json"), get_directory_path("csv"), get_directory_path("data")

download_data_dict = {
    "recovered_url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
    "confirmed_cases_url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "death_url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
}

for data_url in download_data_dict.values():
    download_data(csv_dir, data_url)

alpha3 = get_alpha3(data_dir, "country_codes")

datasets = [{"output": "recovery_data", "input": "time_series_covid19_recovered_global"},
            {"output": "confirmed_deaths_data", "input": "time_series_covid19_deaths_global"},
            {"output": "confirmed_cases_data", "input": "time_series_covid19_confirmed_global"}]

for dataset in datasets:
    ccse_data_to_json(csv_dir, json_dir, dataset["output"], alpha3, dataset["input"])
