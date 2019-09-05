import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy.optimize as opt

def sum_weights(item, weights):
    return sum([weights[x] for x in item['genre']])

genres = pd.read_json('genre_list.json')
dumb_weights = {x:1.0 for x in genres}

# load data here

results = opt.curve_fit
