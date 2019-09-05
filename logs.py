import numpy as np
import pandas as pd

cube = pd.read_json('cube.json')
cube['ln_global_sales'] = np.log(cube['global_sales'])
cube['ln_na_sales'] = np.log(cube['na_sales'])
cube['ln_ja_sales'] = np.log(cube['ja_sales'])
cube['ln_rest_sales'] = np.log(cube['rest_sales'])

cube.to_json('cube_ln.json')
