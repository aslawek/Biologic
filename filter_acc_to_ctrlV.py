import pandas as pd
import numpy as np

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
    global data_filtered

    data_var_name = input('Enter your dataframe name (global variable) or file name: ')
    if data_var_name in globals():
        data = globals()[data_var_name]
        print(f'Read dataframe called {data_var_name}')
    elif data_var_name:
        data = pd.read_csv(data_var_name, sep='\t')
        print(f'Read data from file:\n{data}')
    else:
        print(f"Couldn't find any data called {data_var_name} :(")
        return None

    read_V = float(input('Give me the value of control/V to filter: '))
    err_V = 0.01

    data_filtered = data.loc[(data['control/V'] > read_V - err_V) & (data['control/V'] < read_V + err_V)].reset_index()

    print(f'I just filtered your data according to control/V, from {read_V - err_V} to {read_V + err_V} :)')
    print(f'Filtered data: \n {data_filtered}')

    return data_filtered

del(main)