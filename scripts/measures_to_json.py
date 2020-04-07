import os
import pandas as pd

json_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'json'))
csv_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'csv'))
data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))

df = pd.read_csv(f'{data_dir}/containment_measures.csv')
df = df.drop(columns=['ID', 'Applies To', 'Exceptions','Target state', 'Target region', 'Target country', 'Target city'])
df.to_json(f'{data_dir}/containment_json.json', force_ascii=False, orient='records')