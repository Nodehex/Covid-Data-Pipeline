import requests
import os
import io
import pandas as pd

class GetData():
    directory = os.path.dirname(os.path.abspath(__file__)) + '/csv'

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

    def compare_data(self):
        self.set_old_data()
        if self.old_data is None:
            self.save_to_file() 
            return
        new_columns = self.data.columns
        for column in self.old_data.columns:
            if column not in new_columns:
                print(f'{column} not present in new column')
                return
        self.save_to_file()

    def save_to_file(self):
        print(f'Writing {self.file_name} to file')
        self.data.to_csv(f"{self.directory}/{self.file_name}.csv", na_rep="0")
        print(f'Writing {self.file_name} complete')


# European Center of Disease Control Total Cases
total_cases_url = 'https://covid.ourworldindata.org/data/ecdc/total_cases.csv'
total_cases = GetData(total_cases_url)
total_cases.make_dir()
total_cases.import_data()
total_cases.compare_data()

# European Center of Disease Control Total Cases
new_cases_url = 'https://covid.ourworldindata.org/data/ecdc/new_cases.csv'
new_cases = GetData(new_cases_url)
new_cases.make_dir()
new_cases.import_data()
new_cases.compare_data()

# European Center of Disease Control Total Deaths
total_deaths_url = 'https://covid.ourworldindata.org/data/ecdc/total_deaths.csv'
total_deaths = GetData(total_deaths_url)
total_deaths.import_data()
total_deaths.compare_data()

# European Center of Disease Control Total Deaths
new_deaths_url = 'https://covid.ourworldindata.org/data/ecdc/new_deaths.csv'
new_deaths = GetData(new_deaths_url)
new_deaths.import_data()
new_deaths.compare_data()


# European Center of Disease Control Total Combined
total_combined_url = 'https://covid.ourworldindata.org/data/ecdc/full_data.csv'
total_combined = GetData(total_combined_url)
total_combined.import_data()
total_combined.compare_data()