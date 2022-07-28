import pandas as pd

def load_from_mpt(filename):

    # If you load "raw" Biologic .mpt then it will automatically find how many rows have to be skipped
    if open(filename).readline().rstrip('\n') == 'EC-Lab ASCII FILE':
        rows_to_skip = int(open(filename).readlines()[1].split()[-1]) - 1
        print(f'Got raw EC-Lab ASCII FILE, skipping {rows_to_skip} rows...')
    else:
        rows_to_skip = 0
        print(f'Got something else than EC-Lab ASCII FILE, no rows skipped.')

    # Check label for current column (for CV is different than for CA)
    labels = open(filename).readlines()[rows_to_skip]
    if labels.__contains__('I/mA'):
        label_I = 'I/mA'
    elif labels.__contains__('<I>/mA'):
        label_I = '<I>/mA'
        print(f'Changed column header for current from {label_I} to I/mA')

    # Acutally loading of the data:
    data = pd.read_csv(f'{filename}', encoding="ISO-8859-1", skiprows=rows_to_skip, sep='\t')[
        ['time/s', 'control/V', 'Ewe/V', label_I]] \
        .rename(columns={'<I>/mA': 'I/mA'})

    # Change '.' for "," for all columns (if needed):
    for column in data:
        if data[column].dtype == object:
            data[column] = data[column].str.replace(',', '.').astype(float)

    return data