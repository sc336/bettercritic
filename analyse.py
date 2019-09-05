import pandas as pd
import numpy as np

FILTER = 'baseplatform'
FILTER_VALUE = 'xbox-one'
GROUP_BY = 'source'

cube = pd.read_json('cube.json')

df_source = cube[FILTER_VALUE == cube[FILTER]]
df_source = df_source[False == df_source['duplicates']]
df_results = pd.DataFrame(columns=[GROUP_BY, 'PMCC', 'n'])

for p in df_source[GROUP_BY].drop_duplicates().to_list():
    d = df_source[p == df_source[GROUP_BY]][['global_sales', 'score']]
    n = d.count()['score']
    c = d.corr().iloc()[0,1]
    x = {GROUP_BY : p, 'PMCC' : c, 'n' : n}
    print(x)
    df_results = df_results.append(x, ignore_index=True)

print(df_results[25 < df_results['n']].sort_values(by=['PMCC']))
