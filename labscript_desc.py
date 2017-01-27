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

def format_numerical_param(x):
    """return numerical parameter as string"""
    if abs(x) > 1:
        y = x
        extra = ''
    elif x < 1 and x > 1e-3:
        y = 1e3 * x
        extra = 'm'
    elif x < 1e-3 and x > 1e-6:
        y = 1e6 * x
        extra = 'mu'
    else:
        print(x)
    return "{:.3f}{}".format(y, extra)


def full_output(run_info):
    _str = ''
    for k, v in run_info.items():
        if len(v) > 1:
            _str += 'Run {}:\n'.format(k)
            for kk, vv in v.items():
                param_str = ','.join(format_numerical_param(i) for i in vv)
                _str += '  Param {}\n'.format(kk)
                _str += '    Values: {}\n'.format(param_str)
                _str += '    Min: {}\n'.format(format_numerical_param(min(vv)))
                _str += '    Max: {}\n'.format(format_numerical_param(max(vv)))
                _str += '    Len: {}\n'.format(len(vv))
            _str += ''.join('#' for i in range(50)) + '\n'

    return _str

def summary_ouput(run_info):
    form_str = '{0:40}|{1:40}\n'
    _str = form_str.format('Run','Scan Params')
    _str += ''.join('-' for i in range(80)) + '\n'
    for k, v in run_info.items():
        if len(v) > 1:
            _str += form_str.format(k, ', '.join(i for i in v))

    return _str

def dict_equal(d1, d2):
    #first check if keys are equal
    if d1.keys() != d2.keys():
        return False, False
    else:
        same_vals = True
        for k,v in d1.items():
            try:
                if v != d2[k]:
                    same_vals = False
            except ValueError:
                if v.all() != d2[k].all():
                    same_vals = False
        return True, same_vals

def find_same_scans(run_info):
    #get list of tuples with same scan params
    # dict isn't hashable so can't use set, will use stupid algorithm, but will be find for low numbers
    a = {k:v for k,v in run_info.items() if len(v) > 1}
    keys = list(a.keys())
    ans = []
    for i in range(len(a)-1):
        key = keys.pop(0)
        for k,v in a.items():
            same_keys, same_values = dict_equal(a[key], v)
            if same_keys and k != key:
                ans.append([key,k, same_values])

    _str = "Scans with same scanned parameters are :\n"
    for i in ans:
        _str += "{}, {} :\n Same vals : {}\n".format(i[0],i[1],i[2])

    return _str
def main(folder_path):
    all_files = os.listdir(folder_path)
    runs = set([get_run_name(i) for i in all_files])
    #now for the runs, get scan variable 
    run_info = OrderedDict()
    for run in runs:
        run_info[run] = get_run_info(run, folder_path)
    #now create output
    _str = "Total of {} shots, with {} runs\n".format(len(all_files), len(runs))
    #_str += full_output(run_info)
    _str += summary_ouput(run_info)
    _str += find_same_scans(run_info)
    print(_str)
    


if __name__ == '__main__':
    FOLDERPATH = '/home/zacharyglassman/Downloads/11/'
    main(FOLDERPATH)