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
    
    
def retrEnz(res):
    return res[0]

def retrSubs(res):
    return res[1]


def threadEnzSub(en, sub_subs):
    #print(en.no)
    for sub in sub_subs:
        #if sub.status > 0:
        #    return [en, sub_subs]
        asd = 'no'
        if en.obj.getDistance(sub.obj) < 1:
            asd = 'yes'
            sub.status = 10
            en.status = 10
            #print(sub.no,':', en.no,':',asd)
        #    a = [en, sub_subs]
        #    return a
        #print(sub.no,':', en.no,':',asd)
    a = [en, sub_subs]
    return a

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
    
    time_range = 5 #number of steps
    cell_rad = 1 #radius of cell, currently has no specified unit
    sub_count = 4 #number of substrates
    enz_count = 4
    
    for s in range(0,enz_count):
            enz.append(fun.createEnz(cell_rad, ENZ_A, 1))
    
    for s in range(0,sub_count):
        subs.append(fun.createSub(cell_rad, SUB_A, 1))
    
    i= 0
    for en in enz:
        en.no = i
        i += 1
        #print(en.no)
    i= 0
    for sub in subs:
        sub.no = i
        i += 1
    time = 0
    while time < time_range:
        pass
        sublist = chunkify(subs,len(enz))
        #print(sublist)
        for lst in sublist:
            for sub in lst:
                pass
                #print(sub.no) 
        #print(sublist)
        
        '''

        Calculations come here
        '''
        for en in enz:
            en.status = 0
        #each sublist iteration
        for i in range (0,1):
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
            sublist = hashList(sublist, 0)
            pool = Pool(len(enz))
            results = pool.starmap(threadEnzSub, zip(enz,sublist)) #WARNING! results contains 4
            #sublists, and each of them contains an enzyme and a substrate sublist. Now
            #we need to release them.
            #why not do it... parallelly? :'D
            print(results)
            #print(results)
            j=0
            
            for pack in results:
                enz[j] = pack[0]
                sublist[j] = pack[1]
                j+=1
            
            sublist = hashList(sublist, 1)   
            results = pool.starmap(threadEnzSub, zip(enz,sublist))
            j=0
            print(results)
            for pack in results:
                enz[j] = pack[0]
                sublist[j] = pack[1]
                j+=1 
            
            sublist = hashList(sublist, 2)   
            results = pool.starmap(threadEnzSub, zip(enz,sublist))
            print(results) 
            j=0  
            for pack in results:
                enz[j] = pack[0]
                sublist[j] = pack[1]
                j+=1 
            
            sublist = hashList(sublist, 3)   
            results = pool.starmap(threadEnzSub, zip(enz,sublist))
            print(results)
            j=0
            for pack in results:
                enz[j] = pack[0]
                sublist[j] = pack[1]
                j+=1     
            
            pool.close()
            pool.join()
            #print(results)
            #print("-----ENZYME STATUSES-----")
            #for en in enz:
            #    print(en.status)
            #for o in range(0, len(proc)):
            #    proc[o].join()
            #calculate them
            #join them
        print("time:",time)
        
        time += 1
    #for en in enz:
    #    print("----------------")
    #    print(en.status)
    #for subl in sublist:
    #    for sub in subl:
    #        if sub.status > 0:
    #            print("#######")
    #            print(sub.status)
if __name__ == '__main__':
    main()