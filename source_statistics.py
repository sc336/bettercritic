import pandas as pd
import numpy as np
import datetime

GROUP_BY = 'source'

cube = pd.read_json('cube_ln.json')

df_results = pd.DataFrame(columns=[GROUP_BY, 'mean', 'std', 'skewness', 'n'])

for source in cube[GROUP_BY].drop_duplicates().to_list():
    d = cube[source == cube[GROUP_BY]][['ln_global_sales', 'score']]
    n = d.count()['score']
    mu = d.mean()['score']
    sigma = d.std()['score']
    skew = d.skew()['score']
    x = {GROUP_BY : source, 'mean' : mu, 'std' : sigma, 'skewness' : skew, 'n' : n}
    df_results = df_results.append(x, ignore_index=True)

now = datetime.datetime.now()
filename = "critic_statistics-" + now.strftime("%Y%m%d-%H_%M_%S")
df_results.to_json(filename + '.json')
df_results.to_csv(filename + '.csv')
