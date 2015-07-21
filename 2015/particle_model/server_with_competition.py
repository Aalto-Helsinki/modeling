'''
The main simulation file.
Trying to implement comtetition..
'''
will_plot = 0

#import objects
from vector2 import *
from fileio_alt import *
from objects_revised import *
import math
import copy
import time as tm
import numpy as np
import scipy as sp
from scipy.stats import norm
try:
    import matplotlib.pyplot as plot
    print("Matplotlib detected, will plot...")
    will_plot = 1
except:
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

def transformsub(sub,enz,prob,new_mass):
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

def createEnz(cell_rad,dct):
    '''
    Creates an enzyme object that can then be appended to a list.
    '''
    x = cell_rad +1
    y = cell_rad +1
    while (x*x + y*y) >= cell_rad*cell_rad:
        x = cell_rad*random.random()
        y = cell_rad*random.random()
    vec = Vector2(x,y)
    ob = Obj(dct['mass'],vec)
    #(self,name, obj, sub_type, prod_type,group_id,r_chance,r_range,busy):
    return Enzyme(dct['name'],ob,dct['sub_type'],dct['prod_type'],0,dct['reaction_chance'],dct['reaction_range'],dct['busy'])

def createSupEnz(ob,dct):
    return Enzyme(dct['name'],ob,dct['sub_type'],dct['prod_type'],dct['group_id'],dct['reaction_chance'],dct['reaction_range'],dct['busy'])


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
    fio = fileIO()
    time1 = tm.time()
    try:
        const_filename = sys.argv[1]
    except:
        print("The filename for settings was not specified! Shutting down...")
        return -1
    constants_container = fio.loadFile(const_filename)
    for dct in constants_container:
        print(dct)
    #Load general settings first
    a = 0
    for dct in constants_container:
        if dct["MODULE_TYPE"] == 'settings':
            cell_radius = dct['cell_rad']
            step_amount = dct['step_amount']
            dt = dct['dt']
            spare_amount = dct['spare_table']
    #the  basic settings are now loaded, now to load enzymes and substrates
    spare_index = 0
    #creation of substrates
    substrates = []
    sub_cont = []
    for dct in constants_container:
        if dct['MODULE_TYPE'] == 'substrate':
            sub_cont.append(dct)
    for dct in sub_cont:
        for i in range(0,dct['amount']):
            substrates.append(createSub(cell_radius, dct['type'], dct['mass']))
    
    
    #creation of enzymes, which is a bit trickier...
    enzymes = []
    enz_cont = []
    #separate the enzyme blocks for further processing
    for dct in constants_container:
        if dct['MODULE_TYPE'] == 'enzyme':
            enz_cont.append(dct)
    #and the whole creation of enzymes... shiiiiit
    #collect the different group id:s
    groups = []
    for dct in enz_cont:
        if dct['group_id'] not in groups and dct['group_id'] != 0:
            groups.append( dct['group_id'] )
    for dct in enz_cont:
        #first the easy, not nasty ones (i.e. the ones
        #with no group id
        if dct['group_id'] == 0:
            for i in range(0, dct['amount']):
                enzymes.append(createEnz(cell_radius, dct))
    for group_id in groups:
        #gather the right mass for the group
        m = 0.0
        group = []
        for dct in enz_cont:
            if dct['group_id'] == group_id:
                group.append(dct)
                m += dct['mass']
        #check every particle amount is the same
        am = group[0]['amount']
        for dct in group:
            if am != dct['amount']:
                raise Exception("Joined enzymes amounts don't match! check the settings file",am,dct['amount'])
        for i in range(0,group[0]['amount']):
            #create object
            ob = createPos(cell_radius, m)
            #create enzymes
            for dct in group:
                enzymes.append(createSupEnz(ob, dct))
    #create substrate mass table
    sub_mass = {}
    for dct in sub_cont:
        sub_mass[dct['type']] = dct['mass']
    
    enz_mass = {}
    #should this be a dictionary with enzyme names and masses? YESH
    for enz in enzymes:
        if enz.name not in enz_mass:
            enz_mass[enz.name] = enz.obj.mass
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
    sub_k_values = {}
    for key in sub_mass:
        rad = 0.066*sub_mass[key]**(1/3)*1e-9*2
        print(rad)
        D = 310*1.38e-23/(3*0.7e-3*3.1415*rad)
        print(D)
        sub_k_values[key] = (2*D*dt)**(1/2)
        print(sub_k_values[key])
    #print(sub_k_list)
    
    enz_k_values = {}
    for key in enz_mass:
        rad = 0.066*enz_mass[key]**(1/3)*1e-9
        print(rad)
        D = 1.38e-23*310/(3*3.1415*1.0e-3*rad)
        print(D)
        enz_k_values[key] = (2*D*dt)**(1/2)
        print(enz_k_values[key])
    enz_movements = []
    sub_movements = []
    for i in range(0,len(enzymes)):
        movements_x = norm.rvs(size = spare_amount).tolist()
        movements_y = norm.rvs(size = spare_amount).tolist()
        mov = [movements_x,movements_y]
        enz_movements.append(mov)
            
    for i in range(0,len(substrates)):
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
    sub_amounts = []
    for key in sub_k_values:
        list = []
        sub_amounts.append(list)
    step = 0
    #debugging, let's check out the movements of a few particles
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
            dx = sub_movements[k][0][step%spare_amount]*sub_k_values[sub.type]
            dy = sub_movements[k][1][step%spare_amount]*sub_k_values[sub.type]
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
                dx = spare_movements[0][spare_index%spare_amount]*sub_k_values[sub.type]
                dy = spare_movements[1][spare_index%spare_amount]*sub_k_values[sub.type]
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
            dx = enz_movements[k][0][step%spare_amount]*enz_k_values[enz.name]
            dy = enz_movements[k][1][step%spare_amount]*enz_k_values[enz.name]
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
                dx = spare_movements[0][spare_index%spare_amount]*enz_k_values[enz.name]
                dy = spare_movements[1][spare_index%spare_amount]*enz_k_values[enz.name]
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
                    if sub.status == 0 and sub.type == enz.sub_type:
                        bonded = 0
                        dist = math.hypot(enz.obj.position.x-sub.obj.position.x,enz.obj.position.y-sub.obj.position.y)
                        #if enz.obj.getDistance(sub.obj) < enz_range[enz.type] and enz.type == sub.type :
                        if dist < enz.react_range and enz.sub_type == sub.type :
                            bonded = transformsub(sub,enz, enz.react_chance,sub_mass[enz.prod_type])
                        if bonded > 0:
                            react_ams +=1
                            #print("final sub for this enz:",substrates.index(sub ))
                            enz.status = enz.busy
                            sub.status = enz.busy
                            '''
                            if sub.type == SUB_T_FINAL:
                                if replenish == 1:
                                    products.append(copy.deepcopy(sub))
                                    sub.transform(0,sub_mass[0])
                                else:
                                    products.append(sub)
                                    substrates.remove(sub)
                            '''
                            break
        #collect data
        for i in range(0,len(sub_amounts)):
            a = 0
            for sub in substrates:
                if i == sub.type-1:
                    a += 1     
            sub_amounts[i].append(a)
        step += 1
        print(step)
        #add values for graphs
        '''
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
        '''
    cols = ['r','g','b','c','m','k','r']
    
    time2 = tm.localtime()
    print("simulation took", tm.time()-time1,"seconds")
    #write simulation results to a file
    strfile = fio.writeOutput(sub_amounts)
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
        plot.plot(enzymes[0].react_range*np.cos(cir),enzymes[0].react_range*np.sin(cir))
        plot.plot(sub_x_mov,sub_y_mov,'g')
        plot.plot(enz_x_mov,enz_y_mov,'r')
        #plot.show()
    '''   
    for val in sub_plot_values:
        plot.plot(val,cols[sub_plot_values.index(val)])
    plot.show()
    '''
    #plotting over

if __name__ == '__main__':
    main()
