import matplotlib.pyplot as plt
import pandas as pd

cube = pd.read_json('cube_closefit.json')
cube = cube.sort_values('tsn_ln_global_sales')

def quickplot(data):
    fig, ax = plt.subplots()
    for (label, axis) in data:
        ax.plot([x for x in cube[axis]], label=label)

    legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
    legend.get_frame().set_facecolor('C0')
    plt.show()

