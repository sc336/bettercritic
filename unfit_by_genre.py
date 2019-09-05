import pandas as pd
import numpy as np
import scipy.optimize as opt
import datetime
import math
import tx_quantiles
import sys
import truncated_skewnorm
truncskewnorm = truncated_skewnorm.trunc_skew_norm_gen(name='truncskewnorm')
now = datetime.datetime.now()

amin = np.log(0.01)
def fit_ppf(x, skew, loc, scale):
    print(f"Trying skew={skew}, mu={loc}, sigma={scale}")
    return truncskewnorm.ppf(x, a=(amin-loc)/scale, b=np.inf, skew=skew, loc=loc, scale=scale)

cube = pd.read_json('name-platform-genre-sales.json')

nested_genres = []
list_genres = []
for r in cube['genres'].to_list():
    nested_genres.append(r)
    for x in r:
        list_genres.append(x)
genres = pd.Series( (x for x in list_genres) ).drop_duplicates()
#TODO: This way of handling platforms doesn't seem right.
# EITHER: create a separate model to make a platform-specific factor in the regression
# OR cut the data with platform as a line-item, rather than listed like this
nested_platforms = []
list_platforms = []
for r in cube['baseplatforms'].to_list():
    nested_platforms.append(r)
    for x in r:
        list_platforms.append(x)

df_results = pd.DataFrame(columns=['platform', 'genre', 'mean', 'std', 'skewness', 'n'])

cartesian_magnitude = len(list_platforms) * len(genres)
i = 0
for platform in list_platforms:
    for genre in genres:
        genre_include = [genre in r for r in nested_genres] #Creates a boolean list of rows to include based on presence of genre
        platform_include = [platform in r for r in nested_platforms] #Creates a boolean list of rows to include based on presence of platform

        #Seems to work but test this!
        df_source = pd.DataFrame(cube[genre_include and platform_include])
        df_source = pd.DataFrame(df_source[df_source['global_sales'] > 0])
        df_source['ln_global_sales'] = np.log(df_source['global_sales'])
        n = len(df_source['ln_global_sales'])
        q = tx_quantiles.tx_quantiles(len(df_source['ln_global_sales']))
        mu = df_source['ln_global_sales'].mean()
        sigma = df_source['ln_global_sales'].std()
        skew = df_source['ln_global_sales'].skew()

        x = {'platform': platform, 'genre' : genre, 'mean' : mu, 'std' : sigma, 'skewness': skew, 'n' : n}
        df_results = df_results.append(x, ignore_index=True)
        now = datetime.datetime.now()
        filename = "genre_stn_params-" + now.strftime("%Y%m%d-%H_%M_%S")
        df_results.to_json(filename + '.json')
        df_results.to_csv(filename + '.csv')
        i += 1
        print(f"{100*i/cartesian_magnitude}% done")

filename = "genre_stn_params-" + now.strftime("%Y%m%d-%H_%M_%S")
df_results.to_json(filename + '.json')
df_results.to_csv(filename + '.csv')
