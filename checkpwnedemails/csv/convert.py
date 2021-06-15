import pandas as pd

with open('dehashed.json', encoding='utf-8-sig') as f_input:
    df = pd.read_json(f_input)

df.to_csv('dehashed.csv', encoding='utf-8', index=False)
