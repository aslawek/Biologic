import matplotlib.pyplot
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import asyncio
mpl.use('Qt5Agg'); #mpl.use('TkAgg')

try:
    data
except:
    exit("There is no data loaded. Use load_data.py script.")
else:
    print(f'Data loaded!')

x_arr = []

# sth similar to IIFE
main = lambda f: f(data)
@main
def main(data):

    def mouse_event(event):
        global data, x, x_arr
        x = event.xdata
        print(f'You picked x{len(x_arr) + 1}: {x}')
        x_arr.append(x)

        if len(x_arr) == 2:
            print(f'\nCutting the data to the time range from {x_arr[0]} to {x_arr[1]}')
            data = data.loc[(data['time/s'] < x_arr[0]) | (data['time/s'] > x_arr[1])]
            fig.clear()
            plt.disconnect(cid)

            # Just for plotting. Needs to be put in some function ;)
            fig.clear()
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
            ax1.set_ylabel("control / V", fontsize=12)
            ax2.set_ylabel("current / mA", fontsize=12)
            ax1.tick_params(axis='x', which='major', labelsize=12)

            # colours to y1 and y2 axis
            ax1.spines['left'].set_color('blue')
            ax1.yaxis.label.set_color('blue')
            ax1.tick_params(axis='y', colors='blue', labelsize=12)
            ax2.spines['right'].set_color('red')
            ax2.yaxis.label.set_color('red')
            ax2.tick_params(axis='y', colors='red', labelsize=12)
            fig.show()

            return data
        return x_arr

    print('\nSet the range of time that you need:')

    plt.close()

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
    ax1.set_ylabel("control / V", fontsize=12)
    ax2.set_ylabel("current / mA", fontsize=12)
    ax1.tick_params(axis='x', which='major', labelsize=12)

    # colours to y1 and y2 axis
    ax1.spines['left'].set_color('blue')
    ax1.yaxis.label.set_color('blue')
    ax1.tick_params(axis='y', colors='blue', labelsize=12)
    ax2.spines['right'].set_color('red')
    ax2.yaxis.label.set_color('red')
    ax2.tick_params(axis='y', colors='red', labelsize=12)

    fig.show()

    cid = fig.canvas.mpl_connect('button_press_event', mouse_event)

del(main)