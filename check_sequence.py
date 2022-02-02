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
    # your sequence
    sequence = []
    return True

del(main)