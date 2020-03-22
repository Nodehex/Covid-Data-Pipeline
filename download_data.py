import csv
import requests
import os

directory = 'csv'
if not os.path.exists(directory):
    os.makedirs(directory)

def download_csv(url, filename):
    print(f'Downloading {filename}')
    data = requests.get(url)
    data.raise_for_status()
    print(f'Writing {filename} to file')
    with open(f'{directory}/{filename}.csv', 'w') as f:
        writer = csv.writer(f)
        for line in data.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))
    print(f'Writing {filename} complete')

total_cases_url = 'https://covid.ourworldindata.org/data/ecdc/total_cases.csv'
download_csv(total_cases_url, 'total_cases')

total_deaths_url = 'https://covid.ourworldindata.org/data/ecdc/total_deaths.csv'
download_csv(total_deaths_url, 'total_deaths')