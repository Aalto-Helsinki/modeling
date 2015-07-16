'''
The main simulation file.
Trying to implement comtetition..
'''
will_plot = 0

#import objects
from vector2 import *
from fileio import *
from objects import *
import math
import copy
import time as tm
import numpy as np
import scipy as sp
from scipy.stats import norm
try:
    import matplotlib.pyplot as plot
    will_plot = 1
except:
    print("No matplotlib detected, will not plot")
    will_plot = 0
import random
from builtins import range
import sys
import datetime
from numpy import linspace

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

def transformsub(sub,prob,new_mass):
    '''
    Transforms a substrate to another.
    '''
    
    a = prob
    if a > 1:
        a = 0.5
    if random.random() < a:
        sub.transform(sub.type +1,new_mass)
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

def updateSpare(spare_list, spare_amount):
    del spare_list
    mov_spare_x = norm.rvs(size = spare_amount).tolist()
    mov_spare_y = norm.rvs(size = spare_amount).tolist()
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
    fio = fileIO()
    try:
        const_filename = sys.argv[1]
    except:
        print("The filename for constants was not specified! Shutting down...")
        return -1
    constants = fio.loadSettings(const_filename)
    time1 = tm.time()
    cell_radius = constants['radius']
    enz_types = constants['enz_types']
    sub_types = enz_types +1
    enz_amount_of_each_kind = constants['enz_amount_per_type']
    enz_amount = enz_amount_of_each_kind*enz_types
    sub_amount = constants['sub_amount']
    step_amount = constants['steps']
    SUB_T_FINAL = sub_types -1
    
    dt = constants['dt']
    time = step_amount*dt
    replenish = constants['replenish']
    enz_mass = constants['enz_mass']
    sub_mass = constants['sub_mass']
    enz_busy = constants['enz_busy']
    enz_prob = constants['enz_prob']
    enz_range= constants['enz_range']
    sub_busy = enz_busy
    if_sup_enz = constants['if_sup_enz']
    #determines the size of a spare movement table, bigger tables mean less function calls, smaller tables
    #mean less memory usage.
    spare_amount = constants['spare_table']
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
            m = 0
            for mass in enz_mass:
                m += mass
            for en in enz_mass:
                en = m
            ob = createPos(cell_radius, m)
            for j in range(0, enz_types):
                enzymes.append(createSupEnz(ob, j))
    #create substrates, only create the first type, since it's the only one in the simulation first
    for i in range(0,sub_amount):
        substrates.append(createSub(cell_radius, 0, sub_mass[0]))
     
    #create movement tables for each particle
    #a way to calculate the displacement is to scale the standard normal distribution with the constant k, that is
    # k = sqrt(dim*D*dt),
    #where dim is the number of dimensions, D is the diffusion constant and dt is the time between each displacement
    #D = K_b*T/(3*eta*pi*d), where
    #K_b = botzmann constant, 1.38e-23
    #T = temperature in kelvin, this is 37 C, or 310 K
    #eta = viscosity of water in SI units, this is approx. 0.7*10^-3
    #d = radius of the particles, this is (3/4pi*mass)^1/3*0.43nm
    #we can calculate the radius from mass, if we assume every particle is approximately the same density (they are comprised from
    #the same elements, so why not
    #this means that we don't actually need a variable for delta 
    #so:
    #K_b = 
    #dim = 2
    #dt = dt
    #d ~= (relativemasstopropane/(4/3*pi))^(1/3)*0.43 nm
    #create radius, dalton, other shit here, and multiply the movement in the movement loop with it.
    #create a list of k-values for both enzymes and substrates, so that we can just scale the movement based on
    #the type of the enz/sub.
    sub_k_list = []
    for m in sub_mass:
        rad = 0.43e-9*((m*(3/4*3.1415))**(1/3))
        D = 310*1.38e-23/(3*0.7e-3*3.1415*rad)
        sub_k_list.append(math.sqrt(2*D*dt))
    #print(sub_k_list)
    
    enz_k_list = []
    if if_sup_enz == 1:
        enz_mass_duplicate = []
        mass = 0
        for m in enz_mass:
            mass += m
        for m in enz_mass:
            enz_mass_duplicate.append(mass)
        for m in enz_mass_duplicate:
            rad = 0.43e-9*((m*(3/4*3.1415))**(1/3))
            D = 310*1.38e-23/(3*0.7e-3*3.1415*rad)
            enz_k_list.append(math.sqrt(2*D*dt))
    else:    
        for m in enz_mass:
            rad = 0.43e-9*((m*(3/4*3.1415))**(1/3))
            D = 310*1.38e-23/(3*0.7e-3*3.1415*rad)
            enz_k_list.append(math.sqrt(2*D*dt))
    #print(enz_k_list)
    
    
    enz_movements = []
    sub_movements = []
    for i in range(0,enz_amount):
        movements_x = norm.rvs(size = spare_amount).tolist()
        movements_y = norm.rvs(size = spare_amount).tolist()
        mov = [movements_x,movements_y]
        enz_movements.append(mov)
            
    
    for i in range(0,sub_amount):
        movements_x = norm.rvs(size = spare_amount).tolist()
        movements_y = norm.rvs(size = spare_amount).tolist()
        mov = [movements_x,movements_y]
        sub_movements.append(mov)

    mov_spare_x = norm.rvs(size = spare_amount).tolist()
    mov_spare_y = norm.rvs(size = spare_amount).tolist()
    spare_movements = [mov_spare_x,mov_spare_y]
    #variance of the force is D = myy*kb*T*4?.
    #the movement is force*t/m
    
    #the lists for particle amounts
    sub_plot_values = []
    for i in range(0, sub_types):
        sub_plot_values.append([])
        pass
    step = 0
    #
    #debugging, let's check out the movements of a few particles
    #
    if will_plot:
        sub_x_mov = []
        sub_y_mov = []
        
        enz_x_mov = []
        enz_y_mov = []
    
    #begin main loop
    react_ams = 0
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
            mass = sub.obj.mass
            dx = sub_movements[k][0][step%spare_amount]*sub_k_list[sub.type]
            dy = sub_movements[k][1][step%spare_amount]*sub_k_list[sub.type]
            x = sub.obj.position.x
            y = sub.obj.position.y
            if step_amount == spare_amount:
                del sub_movements
                sub_movements = []
                for i in range(0,sub_amount): 
                    movements_x = norm.rvs(size = spare_amount).tolist()
                    movements_y = norm.rvs(size = spare_amount).tolist()
                    mov = [movements_x,movements_y]
                    sub_movements.append(mov)
            while ((x+dx)**2 + (y+dy)**2) > cell_radius*cell_radius:
                dx = spare_movements[0][spare_index%spare_amount]*sub_k_list[sub.type]
                dy = spare_movements[1][spare_index%spare_amount]*sub_k_list[sub.type]
                spare_index +=1
            if spare_index == spare_amount:
                spare_movements = updateSpare(spare_movements, spare_amount)
                spare_index = 0
            dpos = Vector2(dx,dy)
            sub.obj.setPosition( sub.obj.getPosition() + dpos)
            k += 1
        k=0
        
        for enz in enzymes:
            mass = enz.obj.mass
            dx = enz_movements[k][0][step%spare_amount]*enz_k_list[enz.type]
            dy = enz_movements[k][1][step%spare_amount]*enz_k_list[enz.type]
            x = enz.obj.position.x
            y = enz.obj.position.y
            if step_amount == spare_amount:
                del enz_movements
                enz_movements = []
                for i in range(0,sub_amount):
                    movements_x = norm.rvs(size = spare_amount).tolist()
                    movements_y = norm.rvs(size = spare_amount).tolist()
                    mov = [movements_x,movements_y]
                    enz_movements.append(mov)
            while ((x+dx)**2 + (y+dy)**2) > cell_radius*cell_radius:
                dx = spare_movements[0][spare_index%spare_amount]*enz_k_list[enz.type]
                dy = spare_movements[1][spare_index%spare_amount]*enz_k_list[enz.type]
                spare_index +=1
            if spare_index == spare_amount:
                spare_movements = updateSpare(spare_movements, spare_amount)
                spare_index = 0
            dpos = Vector2(dx,dy)
            
            enz.obj.setPosition( enz.obj.getPosition() + dpos)
            k +=1
        
        if will_plot:
            sub_x_mov.append(substrates[0].obj.position.x)
            sub_y_mov.append(substrates[0].obj.position.y)
            enz_x_mov.append(enzymes[0].obj.position.x)
            enz_y_mov.append(enzymes[0].obj.position.y)
            
        #check and update bonding
        for enz in enzymes:
            if enz.status == 0:
                for sub in substrates:
                    #print("sub:",substrates.index(sub))
                    if sub.status == 0:
                        bonded = 0
                        dist = math.hypot(enz.obj.position.x-sub.obj.position.x,enz.obj.position.y-sub.obj.position.y)
                        #if enz.obj.getDistance(sub.obj) < enz_range[enz.type] and enz.type == sub.type :
                        if dist < enz_range[enz.type] and enz.type == sub.type :
                            bonded = transformsub(sub, enz_prob[enz.type],sub_mass[sub.type +1])
                        if bonded > 0:
                            react_ams +=1
                            #print("final sub for this enz:",substrates.index(sub ))
                            enz.status = enz_busy[enz.type]
                            sub.status = sub_busy[enz.type]
                            if sub.type == SUB_T_FINAL:
                                if replenish == 1:
                                    products.append(copy.deepcopy(sub))
                                    sub.transform(0,sub_mass[0])
                                else:
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
        if step %500 == 0:
            print(step)
            if step %1000 == 0:
                print("amount of reactions in 1000 steps:",react_ams)
                react_ams=0
                print("number of simulated particles:", len(substrates) + len(enzymes))
    #print(len(enzymes))
    cols = ['r','g','b','c','m','k','r']
    
    time2 = tm.localtime()
    print("simulation took", tm.time()-time1,"seconds")
    #write simulation results to a file
    strfile = fio.writeOutput(sub_plot_values)
    strfile.seek(0,0)
    filenlist = const_filename.split("/")
    filename = filenlist[len(filenlist)-2] + '-' +filenlist[len(filenlist)-1]
    dat =  datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S-%f")
    outputfile = open("data/"+filename+dat+".txt",'w')
    for line in strfile:
        outputfile.write(line)
    strfile.close()
    outputfile.close
    
    #print("sim over")
    #simulation over, start plotting
    if will_plot:
        cir = np.linspace(0, 2*3.1415, 100)
        plot.plot(cell_radius*np.cos(cir),cell_radius*np.sin(cir))
        plot.plot(enz_range[0]*np.cos(cir),enz_range[0]*np.sin(cir))
        plot.plot(sub_x_mov,sub_y_mov,'g')
        plot.plot(enz_x_mov,enz_y_mov,'r')
        plot.show()
    '''   
    for val in sub_plot_values:
        plot.plot(val,cols[sub_plot_values.index(val)])
    plot.show()
    '''
    #plotting over

if __name__ == '__main__':
    main()
