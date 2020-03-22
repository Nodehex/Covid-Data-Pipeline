import os
import pandas as pd

json_dir = 'json'
if not os.path.exists(json_dir):
    os.makedirs(json_dir)

csv_dir = './csv'
for filename in os.listdir(csv_dir):
    if filename.endswith('.csv') or filename.endswith('.py'): 
        csv_path = os.path.join(csv_dir, filename)
        df = pd.read_csv(csv_path, index_col=0)
        df = df.fillna(0)
        filename = filename.split('.')[0]
        df.to_json(f'./{json_dir}/{filename}.json')