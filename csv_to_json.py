import os
import pandas as pd
import json

json_dir = 'json'
csv_dir = './csv'

if not os.path.isdir(csv_dir):
    raise NameError('csv folder doesnt exist')

os.makedirs(json_dir, exist_ok=True)

file_name = 'full_data.csv'
csv_path = os.path.join(csv_dir, file_name)
df = pd.read_csv(csv_path)
df = df.rename(columns={"total_deaths": "deaths", "total_cases": "cases"})
file_name = file_name.split('.')[0]
data = {}
for group in df.groupby(['location']):
    data[group[0]] = { 
            "cases": group[1][["date", "cases"]].values.tolist(),
            "deaths": group[1][["date", "deaths"]].values.tolist(),
        }

open(f'./json/{file_name}.json', 'w').write(json.dumps(data))