import numpy as np
import pandas as pd
import scipy.stats as stats
import truncated_skewnorm
import uniles

print('initialising tsn object')
truncskewnorm = truncated_skewnorm.trunc_skew_norm_gen(name='truncskewnorm')
print('tsn object instantiated')

cube = pd.read_json('cube_ln.json')
print('cube loaded')

# See ipython history for next moves
mu = cube['ln_global_sales'].mean()
sigma = cube['ln_global_sales'].std()
skew = cube['ln_global_sales'].skew()
amin = min(cube['ln_global_sales'])
bmax = max(cube['ln_global_sales'])

print(f'{mu}, {sigma}, {skew}, {amin}, {bmax}')
