import os
from helpers import download_data, get_directory_path
from alpha3 import get_alpha3
from ccse_data_to_json import ccse_data_to_json

json_dir, csv_dir, data_dir = get_directory_path("json"), get_directory_path("csv"), get_directory_path("data")

download_data_dict = {
    "recovered": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
    "confirmed_cases": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "confirmed_deaths": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
}

alpha3 = get_alpha3(data_dir, "country_codes")

for file_name, data_url in download_data_dict.items():
    download_data(csv_dir, data_url, file_name)
    ccse_data_to_json(csv_dir, json_dir, alpha3, file_name, file_name)