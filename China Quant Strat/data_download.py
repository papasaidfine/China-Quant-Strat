# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:50:18 2019

@author: lchen2
"""

from datascraper import investing_api as api
import pandas as pd
import numpy as np


work_dir = r'C:\Users\LCHEN2\WORKSPACE\China Quant Strat'

## load data
df_component = pd.read_excel(work_dir + '\\msci_china_imi_constituents.xlsx')
df_component['key'] = df_component['Asset Name']
df_component.key = [s.replace(' INC', '').replace(' LTD' , '').replace(' CORP', '').replace(' GRP', '').replace(' LIMITED', '') for s in df_component.key]

## turn a complete name into a short name as searching key
def func(string):
    str_list = string.split()
    length = max(2, len(str_list)-1)
    space = ' '
    return space.join(str_list[0:length]) 
df_component.key = [func(s) for s in df_component.key]


srch_result = []
keys = list(df_component.key)  # store remaining key, excluding keys_no_rs
keys_no_rs = []  # store keys 

while len(keys) != 0:
    keys_loop = keys
    for key in keys_loop:
        print('Search for %s' % key)
        try:
            df_temp = api.search(key)
            if isinstance(df_temp, type(None)):    
                keys_no_rs.append(key)  # record key without result
                keys.remove(key)  # remove key from executing list
                print('No search result on key %s' % key)        
            else:
                df_temp['srch_key'] = key
                srch_result.append(df_temp)
                keys.remove(key)
                print('OK')
        except:
            print('Request error')
        print('Remaining keys: %i' % len(keys))
print('All clear')


keys_no_rs = [' '.join(s.split()[0:2]) for s in keys_no_rs]
keys = keys_no_rs
while len(keys) != 0:
    keys_loop = keys
    for key in keys_loop:
        print('Search for %s' % key)
        try:
            df_temp = api.search(key)
            if isinstance(df_temp, type(None)):    
                keys_no_rs.append(key)  # record key without result
                keys.remove(key)  # remove key from executing list
                print('No search result on key %s' % key)        
            else:
                df_temp['srch_key'] = key
                srch_result.append(df_temp)
                keys.remove(key)
                print('OK')
        except:
            print('Request error')
        print('Remaining keys: %i' % len(keys))
print('All clear')





        
srch_result = pd.concat(srch_result)

temp = srch_result[srch_result['pair_type'] == 'equities']
srch_result = temp[temp['flag'] == 'equities']


api.search(df_component['srch_key'])







from multiprocessing import Pool

def f(x):
    return x*x

p = Pool(5)
print(p.map(f, [1, 2, 3]))





