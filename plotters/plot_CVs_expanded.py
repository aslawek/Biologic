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

    figure, axis = plt.subplots(1, 2)

    # plot data on two subplots. Add cycles
    if 'cycle' in data:
        print('Cycles found!')
        # Function to change colors (I have no idea how it works)
        jet = plt.get_cmap('jet')
        colors = iter(jet(np.linspace(0, 1, data['cycle'].max())))
        for cycle in range(data['cycle'].max()):
            color = next(colors)
            data_to_plot = data.loc[data['cycle'] == cycle + 1]
            axis[0].plot(data_to_plot['control/V'], data_to_plot['I/mA'], color=color,
                         label=f'cycle {cycle + 1}')
            axis[1].plot(data_to_plot['control/V'], np.abs(data_to_plot['I/mA']), color=color, label=f'cycle {cycle + 1}')
            axis[0].legend()
            #axis[1].legend()
    else:
        print('No column with cycles found, I will plot everything like an animal...')
        axis[0].plot(data['control/V'], data['I/mA'], color='blue')
        axis[1].plot(data['control/V'], np.abs(data['I/mA']), color='blue')

    # plot arrows indicating direction
    index_max_positive = data.loc[data['cycle'] == 1]['control/V'].idxmax()
    index_max_negative = data.loc[data['cycle'] == 1]['control/V'].idxmin()
    index_min = data.loc[data['cycle'] == 1]['time/s'].idxmin()
    index_max = data.loc[data['cycle'] == 1]['time/s'].idxmax()
    arrow_legth = index_max / 25

    print(index_min)
    print(index_max_positive)
    print(index_max_negative)
    print(index_max)

    # take index of last point of 1st cycle (for max time/s)
    arr_V1 = data.iloc[int(data.loc[data['cycle'] == 1]['time/s'].idxmax()*0.0825)]['control/V']
    arr_I1 = data.iloc[int(data.loc[data['cycle'] == 1]['time/s'].idxmax()*0.0825)]['I/mA']
    arr_dV1 = data.iloc[int(data.loc[data['cycle'] == 1]['time/s'].idxmax()*0.0825 + arrow_legth)]['control/V'] - arr_V1
    arr_dI1 = data.iloc[int(data.loc[data['cycle'] == 1]['time/s'].idxmax()*0.0825 + arrow_legth)]['I/mA'] - arr_I1
    # 2
    arr_V2 = data.iloc[int(data.loc[data['cycle'] == 1]['time/s'].idxmax()*0.4267)]['control/V']
    arr_I2 = data.iloc[int(data.loc[data['cycle'] == 1]['time/s'].idxmax()*0.4267)]['I/mA']
    arr_dV2 = data.iloc[int(data.loc[data['cycle'] == 1]['time/s'].idxmax()*0.4267 + arrow_legth)]['control/V'] - arr_V1
    arr_dI2 = data.iloc[int(data.loc[data['cycle'] == 1]['time/s'].idxmax()*0.4267 + arrow_legth)]['I/mA'] - arr_I1

    # plot arrows
    axis[0].arrow(arr_V1, arr_I1, arr_dV1, arr_dI1, color='black', label='kutas', linewidth=5, head_width=.05, length_includes_head=True, zorder=10)
    axis[0].arrow(arr_V2, arr_I2, arr_dV2, arr_dI2, color='black', label='kutas', linewidth=5, head_width=.05, length_includes_head=True, zorder=10)

    # log scale
    axis[1].set_yscale("log")

    # axis labels
    axis[0].set_xlabel("control / V", fontsize=12)
    axis[1].set_xlabel("control / V", fontsize=12)
    axis[0].set_ylabel("current / mA",   fontsize=12)
    axis[1].set_ylabel("|current| / mA",   fontsize=12)
    axis[0].tick_params(axis='x', which='major', labelsize=12)
    axis[1].tick_params(axis='x', which='major', labelsize=12)

    # square box
    axis[0].set_box_aspect(1)
    axis[1].set_box_aspect(1)

    figure.tight_layout()

    plt.show()

del(main)