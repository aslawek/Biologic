import pandas as pd

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data
    filename = input('Yo! Give me the file path here quickly: ')

    # If you load "raw" Biologic .mpt then it will automatically find how many rows have to be skipped
    if open(filename).readline().rstrip('\n') == 'EC-Lab ASCII FILE':
        rows_to_skip = int(open(filename).readlines()[1].split()[-1]) - 1
        print(f'Got raw EC-Lab ASCII FILE, skipping {rows_to_skip} rows...')
    else:
        rows_to_skip = 0
        print(f'Got something else than EC-Lab ASCII FILE, no rows skipped.')

    data = pd.read_csv(f'{filename}', encoding="ISO-8859-1", skiprows=rows_to_skip, sep='\t')[['time/s', 'control/V', 'Ewe/V', 'I/mA']]

    print(f'Loaded data from file {filename}, here you have some info:\n{data.info}')
    print(f'Much more info:\n{data.describe()}\n')
    print(f'Memory usage for each column (in bytes):\n{data.memory_usage()}')
    print(f'Together, it is {data.memory_usage(index=True).sum()/1024} MB\n')
    #return data