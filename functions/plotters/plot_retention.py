import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

mpl.use('Qt5Agg'); #mpl.use('TkAgg')

# sth similar to IIFE
main = lambda f: f()
@main
def main():

    data_var_name = input('Enter your dataframe name (global variable) or file name: ')
    if data_var_name in globals():
        data = globals()[data_var_name]
    elif data_var_name:
        data = pd.read_csv(data_var_name, sep='\t')
        print(f'Read data from file:\n{data}')
    else:
        print(f"Couldn't find any data called {data_var_name} :(")
        return None


    fig = plt.figure()
    ax1 = fig.add_subplot()

    line1 = ax1.plot(data['time/s']/60, data['I_read/mA'], color='blue', label='set')
    #line2 = ax1.plot(data['cycle'], data['I_reset/mA'], color='red', label='reset')
    ax1.legend()

    # axis labels
    ax1.set_xlabel("time/min", fontsize=12)
    ax1.set_ylabel("current / mA",   fontsize=12)
    ax1.tick_params(axis='x', which='major', labelsize=12)

    fig.show()

del(main)