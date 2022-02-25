import pandas as pd
import numpy as np

try:
    data_filtered
except:
    exit("There is no data filtered loaded. Use filter script.")
else:
    print(f'Data filtered loaded!')

# sth similar to IIFE
main = lambda f: f(data_filtered)
@main
def main(data_filtered):
    global data_time_reads

    print(data_filtered)
    data_time_reads = "Trzeba zrobić"

    return data_time_reads

del(main)