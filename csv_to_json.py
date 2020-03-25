import os
import pandas as pd
import json

json_dir = 'json'
csv_dir = './csv'

if not os.path.isdir(csv_dir):
    raise NameError('csv folder doesnt exist')

os.makedirs(json_dir, exist_ok=True)


cases_name = 'total_cases'
cases_path = os.path.join(csv_dir, f'{cases_name}.csv')

cases = pd.read_csv(cases_path, index_col=0)
cases = cases.unstack().to_frame()
cases.columns = ['cases']

deaths_name = 'total_deaths'
deaths_path = os.path.join(csv_dir, f'{deaths_name}.csv')
deaths = pd.read_csv(deaths_path, index_col=0)
deaths = deaths.unstack().to_frame()
deaths.columns = ['deaths']

df = cases.join(deaths)
df = df.reset_index(level=[1])

data = {}
for group in df.groupby(level=0):
    data[group[0]] = { 
        'cases': group[1][['date', 'cases']].values.tolist(),
        'deaths': group[1][['date', 'deaths']].values.tolist(),
    }

file_name = 'full_data'
open(f'./json/{file_name}.json', 'w').write(json.dumps(data))