import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy.optimize as opt
import sys

core_data = pd.read_json('duplicates2.json')
core_data = core_data[core_data.duplicates == False]
list_basename = core_data.basename.unique()

basename_cut = pd.DataFrame(columns=['basename', 'baseplatforms', 'contentRating', 'genres', 'eu_sales', 'na_sales', 'ja_sales', 'rest_sales', 'global_sales'])

for name in list_basename:
    name_set = core_data[core_data.basename == name][['eu_sales', 'na_sales', 'ja_sales', 'rest_sales', 'global_sales', 'genre', 'baseplatform', 'basename', 'contentRating']]
#    print(name_set)
    if len(name_set) > 1:
        s = name_set.groupby(['basename']).agg('sum')
        s = s[['eu_sales', 'na_sales', 'ja_sales', 'rest_sales', 'global_sales']]
        # The double [[]] here returns a dataframe with one column rather than a series, so the rows are aggregated over
        # rather than each item
        genres = list(set([item for sublist in core_data['genre'] for item in sublist]))
        #genres = name_set[['genre']].agg(lambda r: set([item for sublist in r for item in sublist]))
        #genres = [x for x in genres.iloc[0]]
        platforms = [x for x in name_set['baseplatform']]
        ratings = [x for x in name_set['contentRating']]
        # Finally, actually store the data

    #Commented below is a way of doing this using Series.  It may be useful at some other time.
        #series_output = pd.Series({'genres':genres,'baseplatforms':platforms, 'basename':name, 'contentRating':ratings})
        #series_output.append(s[['eu_sales', 'na_sales', 'ja_sales', 'rest_sales', 'global_sales']])
#        series_output = pd.Series([name, platforms, ratings, genres].append(s[['eu_sales', 'na_sales', 'ja_sales', 'rest_sales', 'global_sales']]),
#            index=['basename', 'baseplatforms', 'contentRating', 'genres', 'eu_sales', 'na_sales', 'ja_sales', 'rest_sales', 'global_sales'])
        dict_output = {'basename':name,
            'baseplatforms':platforms,
            'contentRating':ratings,
            'genres':genres,
            'eu_sales':s['eu_sales'].values[0],
            'na_sales':s['na_sales'].values[0],
            'ja_sales':s['ja_sales'].values[0],
            'rest_sales':s['rest_sales'].values[0],
            'global_sales':s['global_sales'].values[0]}

#        print(series_output)
    else:
#        series_output = pd.Series([name_set['basename'], [name_set['baseplatform']], [name_set['contentRating']], [name_set['genre']], name_set['eu_sales'], name_set['na_sales'], name_set['ja_sales'], name_set['rest_sales'], name_set['global_sales']],
#            index=['basename', 'baseplatforms', 'contentRating', 'genres', 'eu_sales', 'na_sales', 'ja_sales', 'rest_sales', 'global_sales'])
        dict_output = {'basename':name_set['basename'].values[0],
            'baseplatforms':name_set['baseplatform'].values,
            'contentRating':name_set['contentRating'].values,
            'genres':list(set(name_set['genre'].values[0])),
            'eu_sales':name_set['eu_sales'].values[0],
            'na_sales':name_set['na_sales'].values[0],
            'ja_sales':name_set['ja_sales'].values[0],
            'rest_sales':name_set['rest_sales'].values[0],
            'global_sales':name_set['global_sales'].values[0]}
        #series_output = pd.Series({'genres':name_set['genre'],'baseplatforms':name_set['baseplatform'], 'basename':name_set['basename'], 'contentRating':name_set['contentRating'],
        #    'eu_sales':name_set['eu_sales'], 'na_sales':name_set['na_sales'], 'ja_sales':name_set['ja_sales'], 'rest_sales':name_set['rest_sales'], 'global_sales':name_set['global_sales']})

#    series_output.name = name
    #basename_cut.loc[name] = series_output
    basename_cut = basename_cut.append(dict_output, ignore_index=True)

basename_cut.to_json('name-platform-genre-sales.json')
