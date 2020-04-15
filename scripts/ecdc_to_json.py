import pandas as pd
import numpy as np
import json

def get_csv_data(csv_dir, file_name, columns_title):
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

def ecdc_to_json(csv_dir, json_dir, file_name, alpha3):

    cases = get_csv_data(csv_dir, 'total_cases', 'cases')
    new_cases = get_csv_data(csv_dir, 'new_cases', 'new_cases')
    cases = cases.join(new_cases)
    cases = get_percentage(cases,'cases')

    deaths = get_csv_data(csv_dir, 'total_deaths', 'deaths')
    new_deaths = get_csv_data(csv_dir, 'new_deaths', 'new_deaths')
    deaths = deaths.join(new_deaths)

    df = cases.join(deaths)
    df.index.names = ['Country', 'date']
    df['death_rate'] = df['deaths'] / df['cases'] * 100
    df = df.fillna(0)

    df = df.rename({'Bonaire Sint Eustatius and Saba': 'Bonaire, Sint Eustatius and Saba', 'Swaziland': 'Eswatini', 
        'Timor': 'Timor-Leste', 'Faeroe Islands': 'Faroe Islands', 'Czech Republic': 'Czechia', 'Macedonia': 'North Macedonia', 'Saint Barthlemy': 'Saint Barthelemy'
        }, level=0)

    df['Country'] = df.index.get_level_values(0)
    df['alpha3'] = df['Country'].map(alpha3)
    df = df.drop(columns='Country')
    df = df.reset_index(level=[1])

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

    open(f'{json_dir}/{file_name}.json', 'w').write(json.dumps(data))
    df.to_csv(f'{json_dir}/{file_name}_processed.csv')

if __name__ == "__main__":
    print('run this from main.py')

