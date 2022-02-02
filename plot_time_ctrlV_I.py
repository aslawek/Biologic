import pandas as pd
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
    ax2 = ax1.twinx()

    line1 = ax1.plot(data['time/s'], data['control/V'], color='blue', label='control / V')
    line2 = ax2.plot(data['time/s'], data['I/mA'], color='red', label='I / mA')

    # added these three lines
    lns = line1 + line2
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=0, fontsize=12)

    # axis labels
    ax1.set_xlabel("time / s", fontsize=12)
    ax1.set_ylabel("control / V",   fontsize=12)
    ax2.set_ylabel("current / mA",  fontsize=12)
    ax1.tick_params(axis='x', which='major', labelsize=12)

    # colours to y1 and y2 axis
    ax1.spines['left'].set_color('blue')
    ax1.yaxis.label.set_color('blue')
    ax1.tick_params(axis='y', colors='blue', labelsize=12)
    ax2.spines['right'].set_color('red')
    ax2.yaxis.label.set_color('red')
    ax2.tick_params(axis='y', colors='red', labelsize=12)

    fig.show()

del(main)