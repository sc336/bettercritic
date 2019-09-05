import numpy as np
import pandas as pd
import scipy.stats as stats
import truncated_skewnorm
import uniles
import sys


print('loading and initialising')
truncskewnorm = truncated_skewnorm.trunc_skew_norm_gen(name='truncskewnorm')
cube = pd.read_json('cube_ln.json')
cube = cube[cube.ln_global_sales.notnull()]
cube = cube.sort_values('ln_global_sales')

print('calculating population statistics')
# See ipython history for next moves
mu = cube['ln_global_sales'].mean()
sigma = cube['ln_global_sales'].std()
skew = cube['ln_global_sales'].skew()
amin = min(cube['ln_global_sales'])
bmax = max(cube['ln_global_sales'])

print(f'mu={mu},\nsigma={sigma},\nskew={skew},\nmin={amin},\nmax={bmax}')

u = uniles.uniles(len(cube['ln_global_sales']))
# Calculates the log global sales, assuming that the score
# is the percentage probability result from a normal CDF
# (ppf is the inverse normal cdf)


#TODO: this save/load thing doesn't actually work - some kind of ValueError on loading
try:
    results = pd.read_json('temp_projection.json')
    start = len(results)
    print(f'loaded {start} results')
except ValueError:
    print('initialising results array')
    results = pd.Series()
    start = 0

print('calculating projections...')
# Too slow!
#cube['projected_ln_global_sales'] = pd.Series(truncskewnorm.ppf(u, a=amin, b=bmax, loc=mu, scale=sigma, skew=skew))
j = start
for i in u[start:]:
    results = results.append(pd.Series(truncskewnorm.ppf(i, a=(amin-mu)/sigma, b=np.inf, loc=mu, scale=sigma, skew=skew)), ignore_index=True)
    j += 1
    if j%1000 == 0:
        print(f'row {j}...')
#        print(results)
        results.to_json('temp_projection.json')
 
cube['projected_ln_global_sales'] = results.values

print('done')
cube.to_json('cube_closefit.json')
