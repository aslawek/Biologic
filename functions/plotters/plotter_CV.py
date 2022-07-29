import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
mpl.use('Qt5Agg'); #mpl.use('TkAgg')

def plotter_CV_simple(data, filename):
    dV_dt = np.around(data["control/V"].diff().abs().sum() / data["time/s"].diff().abs().sum(), 3)
    ax1 = plt.figure().add_subplot()
    ax1.plot(data['control/V'], data['I/mA'], color="blue", label=f'avg dV_dt {dV_dt} V/s')
    ax1.set_title(filename.replace("/", " ").split()[-1])
    ax1.set_xlabel("control / V", fontsize=12)
    ax1.set_ylabel("current / mA", fontsize=12)
    ax1.legend()

def plotter_CV_simple_with_log(data, filename):
    dV_dt = np.around(data["control/V"].diff().abs().sum() / data["time/s"].diff().abs().sum(), 3)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(filename.replace("/", " ").split()[-1])
    ax1.plot(data['control/V'], data['I/mA'], color="blue", label=f'avg dV_dt = {dV_dt} V/s')
    ax2.plot(data['control/V'], np.abs(data['I/mA']), color="red")
    # scales, legend, labels, square box
    ax2.set_yscale("log")
    ax1.legend()
    ax1.set_xlabel("control / V", fontsize=12)
    ax2.set_xlabel("control / V", fontsize=12)
    ax1.set_ylabel("current / mA", fontsize=12)
    ax2.set_ylabel("|current| / mA", fontsize=12)
    ax1.set_box_aspect(1)
    ax2.set_box_aspect(1)
    fig.tight_layout()

def plotter_CV_cycles(data, filename):
    if 'cycle' in data:
        jet = plt.get_cmap('jet')
        colors = iter(jet(np.linspace(0, 1, len(data['cycle'].unique()))))
        ax1 = plt.figure().add_subplot()
        for cycle in data['cycle'].unique():
            data_to_plot = data.loc[data['cycle'] == cycle]
            dV_dt = np.around(data_to_plot["control/V"].diff().abs().sum() / data_to_plot["time/s"].diff().abs().sum(), 3)
            ax1.plot(data_to_plot['control/V'], data_to_plot['I/mA'], color=next(colors),
                     label=f'cycle {cycle}, {dV_dt} V/s')
        ax1.set_title(filename.replace("/", " ").split()[-1])
        ax1.set_xlabel("control / V", fontsize=12)
        ax1.set_ylabel("current / mA", fontsize=12)
        ax1.legend()
    else:
        print('No cycles found.')

def plotter_CV_cycles_with_log(data, filename):
    if 'cycle' in data:
        print('Cycles found!')
        # Function to change colors (I have no idea how it works)
        jet = plt.get_cmap('jet')
        colors = iter(jet(np.linspace(0, 1, len(data['cycle'].unique()))))
        fig, (ax1, ax2) = plt.subplots(1, 2)
        for cycle in data['cycle'].unique():
            data_to_plot = data.loc[data['cycle'] == cycle]
            dV_dt = np.around(data_to_plot["control/V"].diff().abs().sum() / data_to_plot["time/s"].diff().abs().sum(), 3)
            color = next(colors)
            ax1.plot(data_to_plot['control/V'], data_to_plot['I/mA'], color=color, label=f'cycle {cycle}, {dV_dt} V/s')
            ax2.plot(data_to_plot['control/V'], np.abs(data_to_plot['I/mA']), color=color)
        fig.suptitle(filename.replace("/", " ").split()[-1])
        ax2.set_yscale("log")
        ax1.set_xlabel("control / V", fontsize=12)
        ax2.set_xlabel("control / V", fontsize=12)
        ax1.set_ylabel("current / mA", fontsize=12)
        ax2.set_ylabel("|current| / mA", fontsize=12)
        ax1.set_box_aspect(1)
        ax2.set_box_aspect(1)
        fig.tight_layout()
        ax1.legend()
    else:
        print('No cycles found.')

def plotter_CV_direction(data, filename):
    dV_dt = np.around(data["control/V"].diff().abs().sum() / data["time/s"].diff().abs().sum(), 3)
    colors = list(range(data.index.min(), data.index.max() + 1))
    fig, ax1 = plt.subplots()
    cmap = ax1.scatter(data['control/V'], data['I/mA'], marker='.', linewidths=0.2, c=colors, label=f'avg dV_dt {dV_dt} V/s',
                cmap='jet')
    cbar = fig.colorbar(cmap, ticks=[])
    cbar.ax.text(0, data.index.min() - 0.02*data.index.max(), 'start', fontsize=12, ha='left', va='top')
    cbar.ax.text(0, 1.01*data.index.max(), 'end', fontsize=12, ha='left', va='bottom')
    ax1.set_title(filename.replace("/", " ").split()[-1])
    ax1.set_xlabel("control / V", fontsize=12)
    ax1.set_ylabel("current / mA", fontsize=12)
    ax1.legend()

def plotter_CV_direction_cycles(data, filename):
    if 'cycle' in data:
        fig, ax1 = plt.subplots()
        for cycle in data['cycle'].unique():
            data_to_plot = data.loc[data['cycle'] == cycle]
            dV_dt = np.around(data_to_plot["control/V"].diff().abs().sum() / data_to_plot["time/s"].diff().abs().sum(), 3)
            colors = list(range(data_to_plot.index.min(), data_to_plot.index.max() + 1))
            cmap = ax1.scatter(data_to_plot['control/V'], data_to_plot['I/mA'], marker='.', linewidths=0.2, c=colors, label=f'cycle {cycle}, {dV_dt} V/s', cmap='jet')
            cbar = fig.colorbar(cmap, ticks=[]) if cycle == data['cycle'].min() else None
            if cycle == data['cycle'].unique()[0]:
                cbar.ax.text(0, data_to_plot.index.min() - 0.02 * data_to_plot.index.max(), 'start', fontsize=12, ha='left', va='top')
                cbar.ax.text(0, 1.01 * data_to_plot.index.max(), 'end', fontsize=12, ha='left', va='bottom')
        ax1.set_title(filename.replace("/", " ").split()[-1])
        ax1.set_xlabel("control / V", fontsize=12)
        ax1.set_ylabel("current / mA", fontsize=12)
        ax1.legend()
    else:
        print('No cycles found.')