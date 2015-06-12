'''
The main simulation file.
This simulation does not as of yet have any UIs, work is being done to get those.
'''

#import objects
from vector2 import *
#this is for the coming parallel computing
#import multiprocessing
from objects import *
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.stats import norm
import matplotlib.pyplot as plot
import random
from builtins import range

def updateobj(obj, delta, dt):
    x = obj.position.x
    y = obj.position.y
    dx = norm.rvs(scale=delta**2*dt)
    dy = norm.rvs(scale=delta**2*dt)
    while (x+dx)*(x+dx) + (y+dy)*(y+dy) > 100:
        dx = norm.rvs(scale=delta**2*dt)
        dy = norm.rvs(scale=delta**2*dt)
    dpos = Vector2(dx,dy)
    obj.setPosition( obj.getPosition() + dpos)
    #calculate the movement
    #apply the movement

#def updBus(sub):
    #if sub.status > 0:
    #        sub.status -= 1
    #return sub

def transformsub(sub,prob):
    '''
    Transforms a substrate to another.
    '''
    a = prob
    if a > 1:
        a = 0.5
    if random.random() < a:
        sub.transform(sub.type +1)
        return 1
    return 0

def createPos(cell_rad, mass):
    x = cell_rad*random.random()
    y = cell_rad*random.random()
    while (x*x + y*y) >= cell_rad*cell_rad:
        x = cell_rad*random.random()
        y = cell_rad*random.random()
    vec = Vector2(x,y)
    ob = Obj(mass,vec)
    return ob

def createEnz(cell_rad, type, mass):
    '''
    Creates an enzyme object that can then be appended to a list.
    '''
    x = cell_rad +1
    y = cell_rad +1
    while (x*x + y*y) >= cell_rad*cell_rad:
        x = cell_rad*random.random()
        y = cell_rad*random.random()
    vec = Vector2(x,y)
    ob = Obj(mass,vec)
    return Enzyme(ob,type)

def createSupEnz(ob,type):
    return Enzyme(ob, type)


def createSub(cell_rad, type, mass):
    '''
    Creates a substrate object that can then be appended to a list.
    The substrate is placed in a random location inside a circle (cell).
    '''
    x = cell_rad +1
    y = cell_rad +1
    while (x*x + y*y) >= cell_rad*cell_rad:
        x = cell_rad*random.random()
        y = cell_rad*random.random()
    vec = Vector2(x,y)
    ob = Obj(mass,vec)
    return Substrate(ob,type)

def updatePos(part, ):
    pass

def updateSpare(spare_list, spare_amount,delta,dt):
    del spare_list
    mov_spare_x = norm.rvs(size = spare_amount,scale=delta**2*dt).tolist()
    mov_spare_y = norm.rvs(size = spare_amount,scale=delta**2*dt).tolist()
    spare_list = [mov_spare_x,mov_spare_y]
    return spare_list
    
def main():
    #constants that are needed
    #cell size
    #amount of enzyme types
    #amount of substrate types = 1+enzyme types
    #amount of enzymes
    #amount of substrates
    #time range
    #time step
    #delta, is somehow linked to temperature
    #masses of enzymes
    #masses of substrates
    #speed constants of enzymes
    #is this a super_enzyme or normal run
    #enzyme probabilities
    cell_radius = 10
    enz_types = 2
    sub_types = enz_types +1
    enz_amount_of_each_kind = 10
    enz_amount = enz_amount_of_each_kind*enz_types
    sub_amount = 1000
    step_amount = 300
    SUB_T_FINAL = sub_types -1
    
    dt = 0.2
    time = step_amount*dt
    delta = 0.5
    enz_mass = [1,1,1,1,1,1]
    sub_mass = [1,1,1,1,1,1,1]
    enz_busy = [1,1,1,1,1,1]
    enz_prob = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    enz_range=[0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15]
    sub_busy = enz_busy
    if_sup_enz = 1
    #determines the size of a spare movement table, bigger tables mean less function calls, smaller tables
    #mean less memory usage.
    spare_amount = 5000
    spare_index = 0
    #lists that we need
    enzymes = []
    substrates = []
    products = []
    
    #create substrate and enzyme types
    #enzyme type/busyness pairing
    
    #create enzymes
    #this is where the it matters if if_sup_enz is i or 0
    #how to create enzymes? should I create 
    if if_sup_enz == 0:
        for i in range(0,enz_amount_of_each_kind):
            for j in range(0, enz_types):
                enzymes.append(createEnz(cell_radius,j , enz_mass[j]))
    else:
        for i in range(0, enz_amount_of_each_kind):
            ob = createPos(cell_radius, enz_mass[0])
            for j in range(0, enz_types):
                enzymes.append(createSupEnz(ob, j))
    #create substrates, only create the first type, since it's the only one in the simulation first
    for i in range(0,sub_amount):
        substrates.append(createSub(cell_radius, 0, sub_mass[0]))
        
    #create movement tables for each particle
    #the force obeys a normal distribution, with a mean of 0 and a variance of sigma^2.
    #dt is dt, sigma^2 is myy*kb*T*4. 
    #Since brownian motion follows time with a square-root dependency(?), dx = a*dt
    # = f*dt/m
    #these movements are just f*dt, they need to bevalue divided by mass, when we are actually moving
    #the particles
    enz_movements = []
    sub_movements = []
    for i in range(0,enz_amount):
        movements_x = norm.rvs(size = step_amount,scale=delta**2*dt).tolist()
        movements_y = norm.rvs(size = step_amount,scale=delta**2*dt).tolist()
        mov = [movements_x,movements_y]
        enz_movements.append(mov)
            
    
    for i in range(0,sub_amount):
        movements_x = norm.rvs(size = step_amount,scale=delta**2*dt).tolist()
        movements_y = norm.rvs(size = step_amount,scale=delta**2*dt).tolist()
        mov = [movements_x,movements_y]
        sub_movements.append(mov)

    mov_spare_x = norm.rvs(size = spare_amount,scale=delta**2*dt).tolist()
    mov_spare_y = norm.rvs(size = spare_amount,scale=delta**2*dt).tolist()
    spare_movements = [mov_spare_x,mov_spare_y]
    #variance of the force is D = myy*kb*T*4?.
    #the movement is force*t/m
    
    #the lists for particle amounts
    sub_plot_values = []
    for i in range(0, sub_types):
        sub_plot_values.append([])
        pass
    step = 0
    #begin main loop
    while step < step_amount:
        #main loop goes here
        #update particle busynesses
        for en in enzymes:
            en.updBusy()
        for sub in substrates:
            sub.updBusy()
            
        #move particles
            #calculate movement
            #check if applicable, if not, take from spare table
            #make into a vector
            #add
        k=0
        for sub in substrates:
            dx = sub_movements[k][0][step%step_amount]
            dy = sub_movements[k][1][step%step_amount]
            x = sub.obj.position.x
            y = sub.obj.position.y
            
            while ((x+dx)**2 + (y+dy)**2) > cell_radius*cell_radius:
                dx = spare_movements[0][spare_index%spare_amount]
                dy = spare_movements[1][spare_index%spare_amount]
                spare_index +=1
            if spare_index == spare_amount:
                spare_movements = updateSpare(spare_movements, spare_amount, delta, dt)
                spare_index = 0
            dpos = Vector2(dx,dy)
            sub.obj.setPosition( sub.obj.getPosition() + dpos)
            k += 1
        k=0
        
        for enz in enzymes:
            dx = enz_movements[k][0][step%step_amount]
            dy = enz_movements[k][1][step%step_amount]
            x = enz.obj.position.x
            y = enz.obj.position.y
            while ((x+dx)**2 + (y+dy)**2) > cell_radius*cell_radius:
                dx = spare_movements[0][spare_index%spare_amount]
                dy = spare_movements[1][spare_index%spare_amount]
                spare_index +=1
            if spare_index == spare_amount:
                spare_movements = updateSpare(spare_movements, spare_amount, delta, dt)
                spare_index = 0
            dpos = Vector2(dx,dy)
            enz.obj.setPosition( enz.obj.getPosition() + dpos)
            k +=1
        #check and update bonding
        for enz in enzymes:
            if enz.status == 0:
                for sub in substrates:
                    #print("sub:",substrates.index(sub))
                    if sub.status == 0:
                        bonded = 0
                        #dist = math.hypot(enz.obj.position.x-sub.obj.position.x,enz.obj.position.-sub.obj.position.y)
                        if enz.obj.getDistance(sub.obj) < enz_range[enz.type] and enz.type == sub.type :
                            bonded = transformsub(sub, enz_prob[enz.type])
                        if bonded > 0:
                            #print("final sub for this enz:",substrates.index(sub ))
                            enz.status = enz_busy[enz.type]
                            sub.status = sub_busy[enz.type]
                            if sub.type == SUB_T_FINAL:
                                products.append(sub)
                                substrates.remove(sub)
                            break
        #add values for graphs
        amounts = []
        for i in range(0, sub_types):
            amounts.append(0)
        for sub in substrates:
            amounts[sub.type] += 1
        #print(amounts)
        for prod in products:
            amounts[sub_types-1] += 1
        for i in range (0, sub_types):
            sub_plot_values[i].append(amounts[i])
            
        step += 1
        if step %20 == 0:
            print(step)
    print(len(enzymes))
    cols = ['r','g','b','c','m','k','r']
    
    for val in sub_plot_values:
        plot.plot(val,cols[sub_plot_values.index(val)])
    #plot.show()
    
    #simulation over, start plotting
    
    #plotting over

if __name__ == '__main__':
    main()