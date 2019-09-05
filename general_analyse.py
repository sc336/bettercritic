import pandas as pd
import numpy as np
import datetime

GROUP_BY = 'source'

cube = pd.read_json('cube_ln.json')

#This whole nested_genres thing is only required because each item's genre entry is a *list* of applicable genres.
#Analysing by other items should be easier.
nested_genres = []
list_genres = []
for r in cube['genre'].to_list():
    nested_genres.append(r)
    for x in r:
        list_genres.append(x)
genres = pd.Series( (x for x in list_genres) ).drop_duplicates()
print(genres)

df_results = pd.DataFrame(columns=[GROUP_BY, 'genre', 'PMCC', 'Spearman\'s', 'n'])

for genre in genres:
    genre_include = [genre in r for r in nested_genres]

    #Seems to work but test this!
    df_source = cube[genre_include]
    df_source = df_source[False == df_source['duplicates']]     #Some of the data is duplicated in the source; this line excludes them
    #df_results = pd.DataFrame(columns=[GROUP_BY, 'genre', 'PMCC', 'Spearman\'s', 'n'])

    for p in df_source[GROUP_BY].drop_duplicates().to_list():
        d = df_source[p == df_source[GROUP_BY]][['ln_global_sales', 'score']]
        n = d.count()['score']
        c = d.corr().iloc()[0,1]
        s = d.corr('spearman').iloc()[0,1]
        x = {GROUP_BY : p, 'genre' : genre, 'PMCC' : c, 'Spearman\'s' : s, 'n' : n}
        #print(x)
        df_results = df_results.append(x, ignore_index=True)

#    print('\n' + genre)
#    print(df_results[25 < df_results['n']].sort_values(by=['PMCC']))

now = datetime.datetime.now()
filename = "genre_analysis_output-" + now.strftime("%Y%m%d-%H_%M_%S")
df_results.to_json(filename + '.json')
df_results.to_csv(filename + '.csv')
