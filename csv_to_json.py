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

def get_percentage(df, column_factor_name):
    percent_column_name = f'percentage_{column_factor_name}'
    df[percent_column_name] = df[column_factor_name].pct_change(fill_method='ffill')
    df[percent_column_name] = df[percent_column_name].abs() * 100
    df[percent_column_name] = df[percent_column_name].replace({100:0})
    df = df.fillna(0)

    return df

cases = get_csv_data('total_cases', 'cases')
new_cases = get_csv_data('new_cases', 'new_cases')
cases = cases.join(new_cases)
cases = get_percentage(cases,'cases')

deaths = get_csv_data('total_deaths', 'deaths')
new_deaths = get_csv_data('new_deaths', 'new_deaths')
deaths = deaths.join(new_deaths)
deaths = get_percentage(deaths,'deaths')

df = cases.join(deaths)
df = df.fillna(0)
df = df.reset_index(level=[1])

data = {}
for group in df.groupby(level=0):
    data[group[0]] = { 
        'cases': group[1][['date', 'cases']].values.tolist(),
        'newCases': group[1][['date', 'new_cases']].values.tolist(),
        'casesPct': group[1][['date', 'percentage_cases']].values.tolist(),
        'deaths': group[1][['date', 'deaths']].values.tolist(),
        'newDeaths': group[1][['date', 'new_deaths']].values.tolist(),
        'deathsPct': group[1][['date', 'percentage_deaths']].values.tolist(),

    }

file_name = 'full_data'
open(f'./json/{file_name}.json', 'w').write(json.dumps(data))