import csv
import requests
import os

directory = 'csv'
if not os.path.exists(directory):
    os.makedirs(directory)

def download_csv(url, filename):
    data = requests.get(url)

    with open(f'{directory}/{filename}.csv', 'w') as f:
        writer = csv.writer(f)
        for line in data.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))

ecdc_url = 'https://covid.ourworldindata.org/data/ecdc/full_data.csv'

download_csv(ecdc_url, 'ecdc')