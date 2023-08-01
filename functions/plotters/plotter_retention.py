import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
mpl.use('Qt5Agg') #mpl.use('Agg') #mpl.use('TkAgg')

def plotter_retention(data, filename):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(filename.replace("/", " ").split()[-1])
    ax1.plot(data['time/s'], data['I_read/mA'], color='red')
    ax2.plot(data['cycle'], data['I_read/mA'], color="blue")
    # scales, legend, labels, square box
    #ax1.legend()
    ax1.set_xlabel("time / s", fontsize=12)
    ax2.set_xlabel("cycle", fontsize=12)
    ax1.set_ylabel("read current / mA", fontsize=12)
    ax2.set_ylabel("read current / mA", fontsize=12)
    ax1.set_box_aspect(1)
    ax2.set_box_aspect(1)
    fig.tight_layout()