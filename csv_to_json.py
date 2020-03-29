import os
import pandas as pd
import json

json_dir = 'json'
csv_dir = './csv'

if not os.path.isdir(csv_dir):
    raise NameError('csv folder doesnt exist')

os.makedirs(json_dir, exist_ok=True)

def get_csv_data(file_name, columns_title):
    file_path = os.path.join(csv_dir, f'{file_name}.csv')
    data = pd.read_csv(file_path, index_col=0)
    data = data.unstack().to_frame()
    data.columns = [columns_title]
    return data

cases = get_csv_data('total_cases', 'cases')
deaths = get_csv_data('total_deaths', 'deaths')
new_cases = get_csv_data('new_cases', 'new_cases')
new_deaths = get_csv_data('new_deaths', 'new_deaths')

df = cases.join(deaths).join(new_cases).join(new_deaths)
df = df.reset_index(level=[1])

data = {}
for group in df.groupby(level=0):
    data[group[0]] = { 
        'cases': group[1][['date', 'cases']].values.tolist(),
        'deaths': group[1][['date', 'deaths']].values.tolist(),
        'newCases': group[1][['date', 'new_cases']].values.tolist(),
        'newDeaths': group[1][['date', 'new_deaths']].values.tolist(),
    }

file_name = 'full_data'
open(f'./json/{file_name}.json', 'w').write(json.dumps(data))