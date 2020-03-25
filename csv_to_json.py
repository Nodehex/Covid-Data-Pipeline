import os
import pandas as pd

json_dir = 'json'

os.makedirs(json_dir, exist_ok=True)

csv_dir = './csv'

if not os.path.isdir(csv_dir):
    raise NameError('csv folder doesnt exist')

for filename in os.listdir(csv_dir):
    if filename.endswith('.csv'): 
        csv_path = os.path.join(csv_dir, filename)
        df = pd.read_csv(csv_path, index_col=0)
        df = df.fillna(0)
        filename = filename.split('.')[0]
        df.to_json(f'./{json_dir}/{filename}.json',orient='columns')