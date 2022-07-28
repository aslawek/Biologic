import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

mpl.use('Qt5Agg'); #mpl.use('TkAgg')

def plotter_on_offs(data, filename):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    line1 = ax1.plot(data['cycle'], data['I_set/mA'], color='blue', label='set')
    line2 = ax1.plot(data['cycle'], data['I_reset/mA'], color='red', label='reset')
    ax1.legend()
    # axis labels
    ax1.set_title(filename.replace("/", " ").split()[-1])
    ax1.set_xlabel("cycle", fontsize=12)
    ax1.set_ylabel("current / mA",   fontsize=12)
    ax1.tick_params(axis='x', which='major', labelsize=12)

    fig.show()