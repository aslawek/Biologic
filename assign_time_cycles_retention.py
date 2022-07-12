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
    # Put your sequence here:
    sequence = ['bias', 'read']

    print('Hi! I will assign states and group them into cycles according to the sequence:')
    for i in range(len(sequence)):
        print(f'{i+1}\t{sequence[i]}')

    data['cycle'] = np.floor(
        (data['control/V'].ne(data['control/V'].shift()).cumsum() - 1) / len(sequence) + 1).astype('int')
    data['state'] = np.mod(data['control/V'].ne(data['control/V'].shift()).cumsum() - 1, len(sequence)).astype(
        'int')
    for i in range(len(sequence)):
        data['state'].replace({i: sequence[i]}, inplace=True)
    return data

del(main)