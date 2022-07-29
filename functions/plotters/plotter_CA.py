import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('Qt5Agg'); #mpl.use('TkAgg')

def plotter_CA_simple(data, filename):
    ax1 = plt.figure().add_subplot()
    ax2 = ax1.twinx()
    ax1.plot(data['time/s'], data['control/V'], color="blue")
    ax2.plot(data['time/s'], data['I/mA'], color="red")
    ax1.set_title(filename.replace("/", " ").split()[-1])
    ax1.set_xlabel("time / s", fontsize=12)
    ax1.set_ylabel("control / V", fontsize=12)
    ax2.set_ylabel("current / mA", fontsize=12)
    #ax1.legend()

def plotter_CA_points(data, filename):
    ax1 = plt.figure().add_subplot()
    ax2 = ax1.twinx()
    ax1.plot(data['time/s'], data['control/V'], marker='o', color="blue", label=f'test')
    ax2.plot(data['time/s'], data['I/mA'], marker='o', color="red", label=f'test')
    ax1.set_title(filename.replace("/", " ").split()[-1])
    ax1.set_xlabel("time / s", fontsize=12)
    ax1.set_ylabel("control / V", fontsize=12)
    ax2.set_ylabel("current / mA", fontsize=12)
    ax1.legend()