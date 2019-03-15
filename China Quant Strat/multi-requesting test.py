# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 17:18:19 2019

@author: lchen2
"""
import multiprocessing as mul
from time import time
from datascraper import investing_api as api

def f(x):
    return api.search('jpm')

if __name__ == '__main__':
    print("-------- testing multiprocessing on " + str(mul.cpu_count()) + "cores ----------")
    print("")

    elements = 20

    pool = mul.Pool(processes=mul.cpu_count())
    t1 = time()
    res_par = pool.map(f, range(elements))
    t2 = time()
    res_seq = list(map(f, range(elements)))
    t3 = time()
    res_app = [f(x) for x in range(elements)]
    t4 = time()

    print("map() time: " + str(t3-t2) + "s")
    print("pool.map() time: " + str(t2-t1) + "s")
    print("for loop time: " + str(t4-t3) + "s")
    
 
    


