import os
import pandas as pd
import numpy as np
import json

json_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'json'))
csv_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'csv'))

if not os.path.isdir(csv_dir):
    raise NameError('csv folder doesnt exist')

os.makedirs(json_dir, exist_ok=True)

def get_csv_data(file_name, columns_title):
    file_path = f'{csv_dir}/{file_name}.csv'
    data = pd.read_csv(file_path, index_col=0)
    data = data.unstack().to_frame()
    data.columns = [columns_title]
    return data

def get_percentage(df, column_factor_name):
    percent_column_name = f'percentage_{column_factor_name}'
    df[percent_column_name] = df[column_factor_name].pct_change(fill_method='ffill')
    df[percent_column_name] = df[percent_column_name].abs() * 100
    df[percent_column_name] = df[percent_column_name].replace({100:0, np.inf: np.nan})
    df = df.fillna(0)

    return df

cases = get_csv_data('total_cases', 'cases')
new_cases = get_csv_data('new_cases', 'new_cases')
cases = cases.join(new_cases)
cases = get_percentage(cases,'cases')

deaths = get_csv_data('total_deaths', 'deaths')
new_deaths = get_csv_data('new_deaths', 'new_deaths')
deaths = deaths.join(new_deaths)

df = cases.join(deaths)
df.index.names = ['Country', 'date']
df['death_rate'] = df['deaths'] / df['cases'] * 100
df = df.fillna(0)

alpha3 = pd.read_csv('../data/country_codes.csv')
pattern = {',': '','ç': 'c', 'ô': 'o', '’': "'", 'é': ''}
alpha3['Country or Area'] = alpha3['Country or Area'].replace(pattern, regex=True)
alpha3['Country or Area'] = alpha3['Country or Area'].str.replace('\(.*\)', '',regex=True)
alpha3['Country or Area'] = alpha3['Country or Area'].str.replace('\s+the', '',regex=True)
alpha3['Country or Area'] = alpha3['Country or Area'].str.strip()
alpha3 = alpha3.set_index('Country or Area')
alpha3 = alpha3['ISO-alpha3 code']

country_fixes = {'World': 'NA', 'Brunei': 'BRN', 'Czech Republic': 'CZE', 'Vatican': 'VAT', 'United States': 'USA', 'United Kingdom': 'GBR', 'Faeroe Islands': 'FLK', 'International': 'NA', 'Timor': 'TLS', 'Tanzania': 'TZA', 'Kosovo': 'RKS','Taiwan': 'TWN', 'Laos': 'LAO', 'Syria': 'SYR', 'Macedonia': 'MKD', 'Swaziland': 'SWZ', 'Moldova': 'MDA', 'South Korea': 'KOR', 'Palestine': 'PSE', 'Russia': 'RUS', 'Sint Maarten (Dutch part)': 'SXM', 'Saint Vincent and the Grenadines': 'VCT'}
country_fixes = pd.Series(country_fixes)
alpha3 = alpha3.append(country_fixes)

df['Country'] = df.index.get_level_values(0)
df['alpha3'] = df['Country'].map(alpha3)
df = df.drop(columns='Country')
df = df.reset_index(level=[1])

alpha3_dict = df['alpha3'].to_dict()

data = {}
for group in df.groupby(level=0):
    data[group[0]] = {
        'alpha3': group[1]['alpha3'].unique()[0],
        'cases': group[1][['date', 'cases']].values.tolist(),
        'newCases': group[1][['date', 'new_cases']].values.tolist(),
        'casesPct': group[1][['date', 'percentage_cases']].values.tolist(),
        'deaths': group[1][['date', 'deaths']].values.tolist(),
        'newDeaths': group[1][['date', 'new_deaths']].values.tolist(),
        'deathRate': group[1][['date', 'death_rate']].values.tolist(),

    }

file_name = 'full_data'
open(f'{json_dir}/{file_name}.json', 'w').write(json.dumps(data))