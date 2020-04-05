import os
import json
import pandas as pd

json_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'json'))
csv_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'csv'))
data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))

file_name = 'time_series_covid19_recovered_global.csv'
df = pd.read_csv(f'{csv_dir}/{file_name}', index_col=0)
df = df.drop(columns=['Lat', 'Long'])

df = df.reset_index().set_index('Country/Region')
df = df.rename({'Congo (Brazzaville)': 'Congo', 'Congo (Kinshasa)': 'Democratic Republic of Congo'})

def merge_provinces(country_name, df):
    country = df.loc[[country_name]].drop(columns=['Province/State'])
    country = country.sum(axis=0).rename(country_name)
    df = df.drop([country_name]).append(country)
    return df

# Dropping the ships
df = df.drop(['Diamond Princess'])
df = df.drop(['MS Zaandam'])
# Merge countries with provinces into a single row
df = merge_provinces('China', df)
df = merge_provinces('Australia', df)

mask = (df['Province/State'] != '0') & (pd.isnull(df['Province/State']) != True)
df2 = df.loc[mask]
df2 = df2.set_index('Province/State')
df2.index = df2.index.rename('Country/Region')

df = df[(df['Province/State'] == '0') | (pd.isnull(df['Province/State']) == True)]

df = df.append(df2)
df = df.drop(columns='Province/State')

df = df.stack().reset_index(level=1)
df = df.rename(columns={'level_1': 'date', 0: 'recovered'})

df['date'] = pd.to_datetime(df['date']).apply(lambda x: x.strftime('%Y-%m-%d'))

df = df.rename({'Cabo Verde': 'Cape Verde', 'US': 'United States', 'West Bank and Gaza': 'Palestine', 'Burma': 'Myanmar', 'Channel Islands': 'Jersey', 'Holy See': 'Vatican', 'Korea, South': 'South Korea', 'Falkland Islands (Islas Malvinas)': 'Falkland Islands', 'Sint Maarten': 'Sint Maarten (Dutch part)', 'Taiwan*': 'Taiwan','St Martin' :'Saint Martin'})

alpha3 = pd.read_csv('../data/country_codes.csv')
pattern = {'ç': 'c', 'ô': 'o', '’': "'", 'é': 'e'}
alpha3['Country or Area'] = alpha3['Country or Area'].replace(pattern, regex=True)
alpha3['Country or Area'] = alpha3['Country or Area'].str.replace('\(.*\)', '',regex=True)
alpha3['Country or Area'] = alpha3['Country or Area'].str.replace('\s+the', '',regex=True)
alpha3['Country or Area'] = alpha3['Country or Area'].str.strip()
alpha3 = alpha3.set_index('Country or Area')
alpha3 = alpha3['ISO-alpha3 code']

country_fixes = {'World': 'World', 'Brunei': 'BRN', 'Vatican': 'VAT', 'United States': 'USA', 'United Kingdom': 'GBR', 'International': 'International', 'Tanzania': 'TZA', 'Kosovo': 'RKS','Taiwan': 'TWN', 'Laos': 'LAO', 'Syria': 'SYR', 'Moldova': 'MDA', 'South Korea': 'KOR', 'Palestine': 'PSE', 'Russia': 'RUS', 'Sint Maarten (Dutch part)': 'SXM', 'Saint Vincent and the Grenadines': 'VCT'}
country_fixes = pd.Series(country_fixes)
alpha3 = alpha3.append(country_fixes)

df['Country'] = df.index.get_level_values(0)
df['alpha3'] = df['Country'].map(alpha3)
df = df.drop(columns='Country')


data = {}
for group in df.groupby(level=0):
    data[group[0]] = {
        'alpha3': group[1]['alpha3'].unique()[0],
        'recovered': group[1][['date', 'recovered']].values.tolist()
    }

file_name = 'recovery_data'
open(f'{json_dir}/{file_name}.json', 'w').write(json.dumps(data))