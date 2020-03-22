import csv
import requests
import os

if not os.path.exists('data'):
    os.makedirs('data')

def download_csv(url, filename):
    data = requests.get(url)

    with open(f'data/{filename}.csv', 'w') as f:
        writer = csv.writer(f)
        for line in data.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))

ecdc_url = 'https://covid.ourworldindata.org/data/ecdc/full_data.csv'

download_csv(ecdc_url, 'ecdc')