import os
from download_data import download_data


json_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'json'))
csv_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'csv'))
data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))


download_data_dict = {
    # European Centre for Disease Prevention and Control's Data
    'total_cases_url': 'https://covid.ourworldindata.org/data/ecdc/total_cases.csv',
    'new_cases_url': 'https://covid.ourworldindata.org/data/ecdc/new_cases.csv',
    'total_deaths_url': 'https://covid.ourworldindata.org/data/ecdc/total_deaths.csv',
    'new_deaths_url': 'https://covid.ourworldindata.org/data/ecdc/new_deaths.csv',
    'total_combined_url': 'https://covid.ourworldindata.org/data/ecdc/full_data.csv',
    # John Hopkin's Data
    'recovered_url': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
}

for url in download_data_dict.values():
    download_data(csv_dir, url)


# TODO Implement above imports as functions and call them from in here
# TODO  create dir path in here and pass as function arguments to above script files
# TODO Create a function in a separate file that does the alpha3 magic and pass DF as df / save file somewhere idc

import ecdc_to_json
import recovery_to_json