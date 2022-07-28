import pandas as pd
import numpy as np

try:
    data_filtered
except:
    exit("There is no data filtered loaded. Use filter_acc_to_ctrlV.py script.")
else:
    print(f'Data filtered loaded!')

# sth similar to IIFE
main = lambda f: f(data_filtered)
@main
def main(data_filtered):

    # Take median() for time/s change
    time_change_median = data_filtered['time/s'].diff(periods=-1).median()
    print(f'I calculated the change in time/s for every two consecutive points and took median: {time_change_median}')

    # Make copy of global variable and assign state (if the next time/s is larger than 1.1 * median from time change
    data_filtered['cycle'] = data_filtered['time/s'].diff(periods=-1).lt(1.1 * time_change_median).cumsum() + 1

    print(f'Your modified data: \n{data_filtered}')

    return data_filtered

del(main)