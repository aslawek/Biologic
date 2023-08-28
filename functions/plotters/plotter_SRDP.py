import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('Qt5Agg') #mpl.use('Agg') #mpl.use('TkAgg')

def plotter_SRDP_CA_assigning_cycles(data, filename, dt):
    ax1 = plt.figure().add_subplot()
    ax2 = ax1.twinx()
    ax1.plot(data['time/s'], data['I/mA'], color="blue", label=f'current / mA')
    ax2.plot(data['time/s'], data['read_cycle']/data['read_cycle'].max(), color="red", label=f'read / {data["read_cycle"].max()}')
    ax2.plot(data['time/s'], data['peak_cycle']/data['peak_cycle'].max(), color="green", label=f'peak / {data["peak_cycle"].max()}')
    ax1.set_title(f'{filename.replace("/", " ").split()[-1]} dt = {np.round(dt, 3)} s')
    ax1.set_xlabel("time / s", fontsize=12)
    ax1.set_ylabel("current / mA", fontsize=12)
    ax2.set_ylabel("cycle norm.", fontsize=12)
    ax2.legend()
    plt.show()

def plotter_SRDP_I_vs_peak(data, filename, dt):
    jet = plt.get_cmap('jet')
    colors = iter(jet(np.linspace(0, 1, int(len(data['read_cycle'].unique()) / 2))))
    number_of_peaks = data['peak_cycle'].max() / data['read_cycle'].max() * 2
    ax1 = plt.figure().add_subplot()
    for cycle in range(int(data['read_cycle'].max() / 2)):
        data_to_plot = data.loc[(data['peak_cycle'] >= (cycle * number_of_peaks + 1)) & (data['peak_cycle'] <= (number_of_peaks * (cycle + 1)))]
        ax1.plot(data_to_plot['time/s'] - data_to_plot['time/s'].min(), data_to_plot['I/mA'], color=next(colors), label=f'cycle {cycle + 1}')
    ax1.set_title(f'{filename.replace("/", " ").split()[-1]} dt = {np.round(dt, 3)} s')
    ax1.set_xlabel("time (shifted) / s", fontsize=12)
    ax1.set_ylabel("current / mA", fontsize=12)
    ax1.legend()

def plotter_SRDP_reads_peaks_dt(SRDP):
    # Correct
    ax1 = plt.figure().add_subplot()
    ax1.plot(SRDP['dt/s'], SRDP['odd_to_even'], color="blue", label=f'from reads (odd to even)')
    ax1.plot(SRDP['dt/s'], SRDP['first_to_last'], color="red", label=f'from peaks (first to last)')
    # scales, legend, labels, square box
    ax1.set_xlabel("dt / s", fontsize=12)
    ax1.set_ylabel("SRDP ratio", fontsize=12)
    ax1.legend()
    #plt.show()