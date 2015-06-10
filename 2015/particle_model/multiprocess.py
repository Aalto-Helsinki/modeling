'''
A test to check if it is feasible to compute
the simulation parallelly.
'''

from vector2 import *
from multiprocessing import Process,Pool
from objects import *
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.stats import norm
import matplotlib.pyplot as plot
import random
import try_diff_movement as fun
from builtins import range
import time

def chunkify(lst,n):
    return [ lst[i::n] for i in range(n) ]
    
def threadEnzSub(en, sub_subs):
    #print(en.no)
    for sub in sub_subs:
        if sub.status > 0:
            return sub_subs
        asd = 'no'
        if en.obj.getDistance(sub.obj) < 0.5:
            asd = 'yes'
            sub.status = 10
            en.status = 10
            print(sub.no,':', en.no,':',asd)
            return sub_subs
        print(sub.no,':', en.no,':',asd)
    return sub_subs

def hashList(lst,i):
    retval = []
    for k in range(0, len(lst)):
        retval.append(lst[(k+i)%len(lst)])
    return retval

def main():
    '''
    Workflow:
    create a list of substrates
    create a list of enzymes
    create everything else that is needed for the sim.
    
    In the loop:
    for each step:
    create threads, as many as enzymes.
    slice the subs list to as many
    sublists as threads/enzymes
    for i in range(0,threads):
        assign each thread a function, that modifies
        the enzyme and substrate lists as needed
        run these threads
        join
        add i
    after this, join the sublists
    print everything that needs to be printed
    '''
    
    enz = []
    subs = []
    product = []
    
    time_range = 2 #number of steps
    cell_rad = 1 #radius of cell, currently has no specified unit
    sub_count = 400 #number of substrates
    enz_count = 4
    
    for s in range(0,int(enz_count/2)):
            enz.append(fun.createEnz(cell_rad, ENZ_A, 1))
            enz.append(fun.createEnz(cell_rad, ENZ_B, 1))
    
    for s in range(0,sub_count):
        subs.append(fun.createSub(cell_rad, SUB_A, 1))
    
    i= 0
    for en in enz:
        en.no = i
        i += 1
    i= 0
    for sub in subs:
        sub.no = i
        i += 1
    time = 0
    while time < time_range:
        pass
        sublist = chunkify(subs,len(enz))
        for lst in sublist:
            for sub in lst:
                pass
                #print(sub.no) 
        #print(sublist)
        
        '''
        Calculations come here
        '''
        #each sublist iteration
        for i in range (0,len(enz)):
            #with processes
            #create threads
            '''
            proc = []
            for j in range(0,len(enz)):
                proc.append(Process(target = threadEnzSub, args =(enz[j], sublist[(j+i)%len(enz)]) ))
            #start threads
            print("Sublist index:",i)
            for p in proc:
                p.start()
            for p in proc:
                p.join()
            '''    
            #with map and pool:
            #hash the sublist
            #hash the sublist
            #hash the sublist
            sublist = hashList(sublist, i)
            pool = Pool(len(enz))
            results = pool.starmap(threadEnzSub, zip(enz,sublist))
            pool.close()
            pool.join()
            
            #for o in range(0, len(proc)):
            #    proc[o].join()
            #calculate them
            #join them
        print("time:",time)
        
        time += 1
    for sub_subs in sublist:
        for sub in sub_subs:
            print(sub.status)
    for en in enz:
        print(en.status)
    
if __name__ == '__main__':
    main()