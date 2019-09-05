import pandas as pd
import numpy as np
import datetime
import math

cube = pd.read_json('cube_ln.json')

nested_genres = []
list_genres = []
for r in cube['genre'].to_list():
    nested_genres.append(r)
    for x in r:
        list_genres.append(x)
genres = pd.Series( (x for x in list_genres) ).drop_duplicates()
print(genres)

df_results = pd.DataFrame(columns=['platform', 'genre', 'mean', 'std', 'skewness', 'n'])

list_platform = cube['baseplatform'].drop_duplicates()
for platform in list_platform:
    for genre in genres:
        genre_include = [genre in r for r in nested_genres] #Creates a boolean list of rows to include based on presence of genre

        #Seems to work but test this!
        df_source = cube[genre_include]
        df_source = df_source[platform == df_source['baseplatform']]
        df_source = df_source[False == df_source['duplicates']]     #Some of the data is duplicated in the source; this line excludes them
        #df_results = pd.DataFrame(columns=[GROUP_BY, 'genre', 'PMCC', 'Spearman\'s', 'n'])
        d = df_source[['ln_global_sales', 'score']]
#        d = df_source[not math.isnan(df_source['ln_global_sales'])]
        n = d.count()['ln_global_sales']
        mu = d.mean()['ln_global_sales']
        sigma = d.std()['ln_global_sales']
        skew = d.skew()['ln_global_sales']
        x = {'platform': platform, 'genre' : genre, 'mean' : mu, 'std' : sigma, 'skewness': skew, 'n' : n}
        #print(x)
        df_results = df_results.append(x, ignore_index=True)

#    print('\n' + genre)
#    print(df_results[25 < df_results['n']].sort_values(by=['PMCC']))

now = datetime.datetime.now()
filename = "genre_platform_statistics-" + now.strftime("%Y%m%d-%H_%M_%S")
df_results.to_json(filename + '.json')
df_results.to_csv(filename + '.csv')
