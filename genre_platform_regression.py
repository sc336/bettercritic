import numpy as np
import pandas as pd
import scipy.stats as stats
import math
import matplotlib.pyplot as plt
import tx_quantiles

cube_reviews = pd.read_json('cube_ln.json')
cube_titles = pd.read_json('cube_closefit.json')
