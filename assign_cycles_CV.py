import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    data
except:
    exit("There is no data loaded. Use load_data.py script.")
else:
    print(f'Data loaded!')

# sth similar to IIFE
main = lambda f: f(data)
@main
def main(data):
    print('Hi! I will assign cycles to your CV data.')

    # Drop (remove) last row no to have empty (1-point) last CV cycle
    data.drop(data.tail(1).index, inplace=True)
    print(data)

    data['cycle'] = np.ceil(np.sign(data['control/V']).diff().ne(0).astype('int').cumsum() / 2).astype('int')
    print(data)

    return data

del(main)