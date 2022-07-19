import pandas as pd

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data

    list_filenames = [
        'data/ITO_Ni[Me4Benzo]_Cu_el3_CV_scan_rates_01_CV_C01.mpt',
        'data/ITO_Ni[Me4Benzo]_Cu_el3_CV_scan_rates_02_CV_C01.mpt',
        'data/ITO_Ni[Me4Benzo]_Cu_el3_CV_scan_rates_03_CV_C01.mpt',
        'data/ITO_Ni[Me4Benzo]_Cu_el3_CV_scan_rates_04_CV_C01.mpt',
        'data/ITO_Ni[Me4Benzo]_Cu_el3_CV_scan_rates_05_CV_C01.mpt',
        'data/ITO_Ni[Me4Benzo]_Cu_el3_CV_scan_rates_06_CV_C01.mpt',
        'data/ITO_Ni[Me4Benzo]_Cu_el3_CV_scan_rates_07_CV_C01.mpt',
        'data/ITO_Ni[Me4Benzo]_Cu_el3_CV_scan_rates_08_CV_C01.mpt',
        'data/ITO_Ni[Me4Benzo]_Cu_el3_CV_scan_rates_09_CV_C01.mpt',
        'data/ITO_Ni[Me4Benzo]_Cu_el3_CV_scan_rates_10_CV_C01.mpt'
    ]

    if len(list_filenames) == 0:
        print('\nNo element found in list_filenames.')
        return None

    data = pd.DataFrame()

    for index, filename in enumerate(list_filenames):
        ### LOADING DATA ###

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

        data_to_append = pd.read_csv(f'{filename}', encoding="ISO-8859-1", skiprows=rows_to_skip, sep='\t')[
            ['time/s', 'control/V', 'Ewe/V', label_I]] \
            .rename(columns={'<I>/mA': 'I/mA'})

        print(f'Loaded data {index + 1} of {len(list_filenames)} from file {filename}')

        data = pd.concat([data, data_to_append])
        print(data)

    # Change '.' for "," for all columns (if needed):
    for column in data:
        if data[column].dtype == object:
            data[column] = data[column].str.replace(',', '.').astype(float)

    return data

del(main)