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

# sth similar to IFFE
main = lambda f: f()
@main
def main():
    global data

    print('You want to filter data by time range.')
    x1 = float(input('Give me x1: '))
    x2 = float(input('Give me x2: '))

    print(f'\nCutting the data to the time range from {x1} to {x2}')
    data = data.loc[(data['time/s'] > x1) & (data['time/s'] < x2)]
    print(data)
    return data

del(main)