import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('Qt5Agg'); #mpl.use('TkAgg')

# sth similar to IIFE
main = lambda f: f()
@main

def main():
    data_var_name = input('Enter your dataframe name (global variable) or file name: ')
    if data_var_name in globals():
        data = globals()[data_var_name]
        print(f'Read dataframe called {data_var_name}')
    elif data_var_name:
        data = pd.read_csv(data_var_name, sep='\t')
        print(f'Read data from file:\n{data}')
    else:
        print(f"Couldn't find any data called {data_var_name} :(")
        return None

    fig = plt.figure()
    ax1 = fig.add_subplot()

    if 'cycle' in data:
        print('Cycles found!')
        # Function to change colors (I have no idea how it works)
        jet = plt.get_cmap('jet')
        colors = iter(jet(np.linspace(0, 1, data['cycle'].max())))
        for cycle in range(data['cycle'].max()):
            data_to_plot = data.loc[data['cycle'] == cycle + 1]
            line = ax1.plot(data_to_plot['control/V'], data_to_plot['I/mA'], color=next(colors),
                            label=f'cycle {cycle + 1}')
            ax1.legend()
    else:
        print('No column with cycles found, I will plot everything like an animal...')
        line = ax1.plot(data['control/V'], data['I/mA'], color='blue')

    # axis labels
    ax1.set_xlabel("control / V", fontsize=12)
    ax1.set_ylabel("current / mA",   fontsize=12)
    ax1.tick_params(axis='x', which='major', labelsize=12)

    fig.show()

del(main)