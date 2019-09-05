#TODO: think of a better name for this

def tx_quantiles(n):
    s = 1 / (n+1)
    quantiles_list= [(x+1)*s for x in range(n)]
    return quantiles_list
