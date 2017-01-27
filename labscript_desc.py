"""
File to document a day's worth of labscript experiments

"""
import os
import h5py
from collections import OrderedDict
from numpy import linspace, arange

def get_run_name(full_run_name):
    """gets the run name from file in form 
    name_number.h5 
    """
    #now split on _ and keep all but last 
    name_list = full_run_name.rstrip('.h5').split('_')[:-1]
    return '_'.join(i for i in name_list) 

def evaluate_global(x):
    #first check for bool 
    if x in ['True', 'False']:
        return [1]
    #now check if number
    try:
        float(x)
        return [x]
    except:
        #don't know what it is, so check if its a numpy expressions
        try:
            y = eval(x)
            return y
        except:
            print('Could not evaluate {}'.format(x))
            return [1]

def get_run_info_from_file(run, folder_path, number):
    filename = os.path.join(folder_path, "{}_{}.h5".format(run, number))
    ans_dict = {}
    with h5py.File(filename, 'r') as _file:
        for group in _file['globals']:
            for var in _file['globals'][group].attrs:
                ans_dict[var] = evaluate_global(_file['globals'][group].attrs[var])
    return {i:v for i,v in ans_dict.items() if len(v)>1}

def get_run_info(run, folder_path):
    """Need to try many combinations of number to get the correct padding 
    don't a priori know which one it will be 
    """
    number = '0'
    while True:
        try:
            ans = get_run_info_from_file(run, folder_path, number)
            break 
        except:
            #first try to zfill
            if len(number) < 5:
                number = number.zfill(len(number) + 1)
            else:
                #then increment
                number = str(int(number) + 1)
    return ans

def main(folder_path):
    all_files = os.listdir(folder_path)
    runs = set([get_run_name(i) for i in all_files])
    #now for the runs, get scan variable 
    run_info = OrderedDict()
    for run in runs:
        run_info[run] = get_run_info(run, folder_path)
    print("Total of {} shots, with {} runs".format(len(all_files), len(runs)))
    for k,v in run_info.items():
        if len(v) > 1:
            print('Run {}:'.format(k))
            for kk,vv in v.items():
                param_str = ','.join(str(i) for i in vv)
                print('\t Param {} : {}'.format(kk, param_str))


if __name__ == '__main__':
    FOLDERPATH = '/home/zacharyglassman/Downloads/11/'
    main(FOLDERPATH)