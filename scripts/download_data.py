import requests
import os
import io
import pandas as pd

class GetData():
    directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'csv'))

    def __init__(self, url):
        self.url = url
        self.file_name = url.split('/')[-1].split(".")[0]
        self.data = None
        self.old_data = None

    def make_dir(self):
        os.makedirs(self.directory, exist_ok=True)

    def import_data(self):
        print(f"Downloading data for: {self.file_name}")
        data = requests.get(self.url)
        data.raise_for_status()
        data = pd.read_csv(io.StringIO(data.content.decode('utf-8')), index_col=0)
        data = data.fillna(0)
        self.data = data

    def __str__(self):
        return str(self.data.head())

    def set_old_data(self):
        old_filepath = f'{self.directory}/{self.file_name}.csv'
        if os.path.isfile(old_filepath) is False:
            print(f'There doesnt appear to be an old {self.file_name}.')
        else:
            self.old_data = pd.read_csv(old_filepath)

    def save_data(self):
        self.set_old_data()
        if self.old_data is None:
            self.save_to_file() 
            return
        if len(self.data.index) <= len(self.old_data):
            print(f'{self.file_name} has not yet updated. Skipping')
            return
        self.save_to_file()

    def save_to_file(self):
        print(f'Writing {self.file_name} to file')
        self.data.to_csv(f"{self.directory}/{self.file_name}.csv", na_rep="0")
        print(f'Writing {self.file_name} complete')
    
    def download_data(self):
        self.make_dir()
        self.import_data()
        self.save_data()

# European Center of Disease Control Total Cases
total_cases_url = 'https://covid.ourworldindata.org/data/ecdc/total_cases.csv'
total_cases = GetData(total_cases_url)
total_cases.download_data()
# European Center of Disease Control Total Cases
new_cases_url = 'https://covid.ourworldindata.org/data/ecdc/new_cases.csv'
new_cases = GetData(new_cases_url)
new_cases.download_data()

# European Center of Disease Control Total Deaths
total_deaths_url = 'https://covid.ourworldindata.org/data/ecdc/total_deaths.csv'
total_deaths = GetData(total_deaths_url)
total_deaths.download_data()

# European Center of Disease Control Total Deaths
new_deaths_url = 'https://covid.ourworldindata.org/data/ecdc/new_deaths.csv'
new_deaths = GetData(new_deaths_url)
new_deaths.download_data()


# European Center of Disease Control Total Combined
total_combined_url = 'https://covid.ourworldindata.org/data/ecdc/full_data.csv'
total_combined = GetData(total_combined_url)
total_combined.download_data()

# John Hopkin's University Recovered
recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
recovered = GetData(recovered_url)
recovered.download_data()
