import numpy as np
import pandas as pd
import scipy.stats as stats
import truncated_skewnorm
import uniles
import sys


print('loading and initialising')
truncskewnorm = truncated_skewnorm.trunc_skew_norm_gen(name='truncskewnorm')
cube = pd.read_json('name-platform-sales.json')
cube = cube.sort_values('global_sales')
cube['ln_global_sales'] = np.log(cube['global_sales'])
cube = cube[np.isfinite(cube.ln_global_sales)]

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


print('initialising results array')
tsn = pd.Series()
sn = pd.Series()
tn = pd.Series()
start = 0

print('calculating projections...')
# Too slow!
#cube['projected_ln_global_sales'] = pd.Series(truncskewnorm.ppf(u, a=amin, b=bmax, loc=mu, scale=sigma, skew=skew))
j = start
for i in u[start:]:
    tsn = tsn.append(pd.Series(truncskewnorm.ppf(i, a=(amin-mu)/sigma, b=np.inf, loc=mu, scale=sigma, skew=skew)), ignore_index=True)
    sn = sn.append(pd.Series(stats.skewnorm.ppf(i, a=skew, loc=mu, scale=sigma)), ignore_index=True)
    tn = tn.append(pd.Series(stats.truncnorm.ppf(i, a=(amin-mu)/sigma, b=np.inf, loc=mu, scale=sigma)), ignore_index=True)
    j += 1
    if j%1000 == 0:
        print(f'row {j}...')
 
cube['tsn_ln_global_sales'] = tsn.values
cube['sn_ln_global_sales'] = sn.values
cube['tn_ln_global_sales'] = tn.values

print('done')
cube.to_json('cube_closefit.json')
