import pandas as pd

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    input_var_name = input('Enter your dataframe name (global variable): ')
    if input_var_name in globals():
        print(f'"{input_var_name}" found!')
    else:
        print('There is no such global variable :(')
        return None
    output_name = input('Enter the new filename: ')
    print(f'\nHere is your data:\n{globals()[input_var_name]}')
    globals()[input_var_name].to_csv(f'{output_name}', sep='\t', index=False)
    print(f'\nYour dataframe called {input_var_name} was saved as {output_name}')

del(main)