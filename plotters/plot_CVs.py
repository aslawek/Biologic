import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
mpl.use('Qt5Agg'); #mpl.use('TkAgg')

def plot_CVs(data, filename):

    log_scale = False
    show_dV_dt = True
    show_direction = True

    if log_scale == True:
        print('lalala')
    elif log_scale == False:
        fig = plt.figure()
        ax1 = fig.add_subplot()
        if 'cycle' in data:
            print('Cycles found!')
            # Function to change colors (I have no idea how it works)
            jet = plt.get_cmap('jet')
            colors = iter(jet(np.linspace(0, 1, data['cycle'].max())))
            for cycle in range(data['cycle'].max()):
                data_to_plot = data.loc[data['cycle'] == cycle + 1]
                dV_dt = f', {np.around(data_to_plot["control/V"].diff().abs().sum() / data_to_plot["time/s"].diff().abs().sum(), 3)} V/s' if show_dV_dt == True else ""
                ax1.plot(data_to_plot['control/V'], data_to_plot['I/mA'], color=next(colors),
                                label=f'cycle {cycle + 1}{dV_dt}')
                ax1.legend()
                # axis labels
                ax1.set_title(filename.replace("/", " ").split()[-1])
                ax1.set_xlabel("control / V", fontsize=12)
                ax1.set_ylabel("current / mA", fontsize=12)
                ax1.tick_params(axis='x', which='major', labelsize=12)
                fig.show()
        else:
            print('No column with cycles found, I will plot everything like an animal...')
            fig, ax = plt.subplots()
            pcm = ax.scatter(data['control/V'], data['I/mA'], marker='.', c=list(range(data.index.min(), data.index.max() + 1)), cmap='twilight')
            fig.colorbar(pcm, cmap='twilight', ticks=[])
            #fig.show()

    else:
        return None
