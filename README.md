# Biologic
Some scripts for Biologic .mpt data

We use python scripts via PyCharms Python Console by typing runfile(’./<script.py>’).
Most of scripts generate/work on a few global variables e.g. data, something similar as in MatLab environment. Variables containing data (not files) are pandas dataframes and all pandas functions work on such objects

load_data.py – loads data either from file (give path with „/”) or from pandas dataframe (global variable in Python Console). It loads 4 standard columns from biologic .mpt file for CV or CA: time/s, control/V, Ewe/V and I/mA creating global variable called „data” 

save_data.py – saves data from given global variable (pandas dataframe) as a file (for some reason project needs some time to refresh)

filter_acc_to_ctrlV.py - takes the given data (global var) and filters it according to the given value of control/V (+/- standard 0.01 V) 

cut/rm_data_by_plot.py – cuts/removes part of data according to clickable plot

cut/rm_data_by_time_range.py – cuts/removes part of data according to given ranges

assign_states_and_cycles.py – takes „data” dataframe (global var) and assigns state and cycle according to sequence. In practice it checks the change when control/V changes, then loops state assignment

assign_cycle_CV.py - takes "data" dataframe (global var) and assigns cycles according to the sign change of the control/V value (every 2 changes of sign, cycle += 1).

assign_time_reads.py - takes "data_filtered" (global var) and calculate the "standard" time/s change (i.e. median of change in time/s between consecutive datapoints). Adds cycle column. Increases the cycle number if the next point is 1.1 times greater than "standard" time/s change.

extract_on_off.py – for each cycle take all read_set and read_reset points and calculate median(). Returns data_on_off global variable that can be saved as a file

extract_time_reads.py - for each cycle in "data_filtered" (global var) calculate median for I/mA. Split them for I_odd/mA for cycles 1,3,5... and I_even for cycles 2,4,6...

plot_time_ctrlV_I.py - plots either global variable (pandas dataframe) or data from file. Ewe/V and I/mA is a function of time/s

plot_on_off.py – similar but I_set/mA and I_reset/mA is a function of cycle

plot_CVs.py - plots I/mA as a function of control/V. If you numbered subsequent cycles (see assign_cycles_CV.py) it will also rainbow your data.

Enjoy!
