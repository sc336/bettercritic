import numpy as np
import pandas as pd
import scipy.stats as stats
import math
import matplotlib.pyplot as plt
from tx_quantiles import tx_quantiles
import truncated_skewnorm

truncskewnorm = truncated_skewnorm.trunc_skew_norm_gen(name='truncskewnorm')

cube_reviews = pd.read_json('cube_ln.json')
cube_titles = pd.read_json('cube_closefit.json')
