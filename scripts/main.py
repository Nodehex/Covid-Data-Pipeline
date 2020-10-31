import os
import urllib.request
from download_data import download_data
from alpha3 import get_alpha3
from ecdc_to_json import ecdc_to_json
from recovery_to_json import recovery_to_json


json_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'json'))
os.makedirs(json_dir, exist_ok=True)

csv_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'csv'))
os.makedirs(csv_dir, exist_ok=True)

data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
os.makedirs(data_dir, exist_ok=True)

urllib.request.urlretrieve("https://opendata.ecdc.europa.eu/covid19/testing/json/", os.path.join(json_dir, "tests_done.json"))
urllib.request.urlretrieve("https://opendata.ecdc.europa.eu/covid19/hospitalicuadmissionrates/json/", os.path.join(json_dir, "hospitalizations.json"))

download_data_dict = {
    # European Centre for Disease Prevention and Control's Data
    'total_cases_url': 'https://covid.ourworldindata.org/data/ecdc/total_cases.csv',
    'new_cases_url': 'https://covid.ourworldindata.org/data/ecdc/new_cases.csv',
    'total_deaths_url': 'https://covid.ourworldindata.org/data/ecdc/total_deaths.csv',
    'new_deaths_url': 'https://covid.ourworldindata.org/data/ecdc/new_deaths.csv',
    'total_combined_url': 'https://covid.ourworldindata.org/data/ecdc/full_data.csv'
}

for url in download_data_dict.values():
    download_data(csv_dir, url)

alpha3 = get_alpha3(data_dir, 'country_codes')

ecdc_to_json(csv_dir, json_dir, 'full_data', alpha3)
