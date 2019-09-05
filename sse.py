import pandas as pd
import math
import numpy as np

cube = pd.read_json('cube_closefit.json')
cube = cube.sort_values('ln_global_sales')

cube['tsn_residuals'] = cube['ln_global_sales'] - cube['tsn_ln_global_sales']
cube['tn_residuals'] = cube['ln_global_sales'] - cube['tn_ln_global_sales']
cube['sn_residuals'] = cube['ln_global_sales'] - cube['sn_ln_global_sales']

tsn_ssr = sum([x**2 for x in cube['tsn_residuals']])
tn_ssr = sum([x**2 for x in cube['tn_residuals']])
sn_ssr = sum([x**2 for x in cube['sn_residuals']])

tsn_mssr = tsn_ssr/len(cube['ln_global_sales'])
tn_mssr = tn_ssr/len(cube['ln_global_sales'])
sn_mssr = sn_ssr/len(cube['ln_global_sales'])

tsn_rmssr = np.sqrt(tsn_mssr)
tn_rmssr = np.sqrt(tn_mssr)
sn_rmssr = np.sqrt(sn_mssr)

results = pd.DataFrame([['TSN', tsn_ssr, tsn_mssr, tsn_rmssr], ['TN', tn_ssr, tn_mssr, tn_rmssr], ['SN', sn_ssr, sn_mssr, sn_rmssr]], columns=['Model', 'SSR', 'MSSR', 'RMSSR'])

print(results)
