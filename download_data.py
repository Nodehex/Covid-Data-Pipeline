import csv
import requests
import os
import io
import pandas as pd

class GetData():
    directory = 'csv'

    def __init__(self, url):
        self.url = url
        self.file_name = url.split('/')[-1].split(".")[0]
        self.data = None

    def make_dir(self):
        if not os.path.exists(self.directory):
            print("Directory not found. Creating")
            os.makedirs(self.directory)
        else:
            print("Directory already exists")

    def import_data(self):
        print(f"Downloading data for: {self.file_name}")
        data = requests.get(self.url)
        data.raise_for_status()
        data = pd.read_csv(io.StringIO(data.content.decode('utf-8')))
        data = data.fillna(0)
        self.data = data

    def __str__(self):
        return str(self.data.head())

    def compare_data(self, new_data, old_data):
        print(new_data.head())

    def save_to_file(self):
        print(f'Writing {self.file_name} to file')
        self.data.to_csv(f"./{self.directory}/{self.file_name}.csv", index=False)
        print(f'Writing {self.file_name} complete')


# European Center of Disease Control Total Cases
total_cases_url = 'https://covid.ourworldindata.org/data/ecdc/total_cases.csv'
total_cases = GetData(total_cases_url)
total_cases.make_dir()
total_cases.import_data()
print(total_cases)
total_cases.save_to_file()

# European Center of Disease Control Total Deaths
total_deaths_url = 'https://covid.ourworldindata.org/data/ecdc/total_deaths.csv'
total_deaths = GetData(total_deaths_url)
total_deaths.import_data()
total_deaths.save_to_file()
