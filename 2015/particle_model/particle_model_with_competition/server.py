'''
The main simulation file.
'''

#import objects
from vector2 import *
from fileio import *
from objects import *
import math
import copy
import time as tm
import numpy as np
from scipy.stats import norm
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

def transformsub(sub,enz,prob,new_mass,prod_rep):
    '''
    Transforms a substrate to another.
    '''
    a = prob
    if a > 1:
        a = 0.5
    if random.random() < a:
        sub.transform(enz.prod_type,new_mass,prod_rep)
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
    '''
    Creates an enzyme object that can then be appended to a list.
    '''
    return Enzyme(dct['name'],ob,dct['sub_type'],dct['prod_type'],dct['group_id'],dct['reaction_chance'],dct['reaction_range'],dct['busy'])

def createSub(cell_rad, type, mass, rep):
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
    return Substrate(ob,type,rep)

def updateSpare(spare_list, spare_amount):
    '''
    Updates the spare list of gaussian distributed random variables when they are used.
    '''
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
    '''
    for dct in constants_container:
        print(dct)
    '''
    #Load general settings first
    a = 0
    for dct in constants_container:
        if dct["MODULE_TYPE"] == 'settings':
            cell_radius = dct['cell_rad']
            step_amount = dct['step_amount']
            dt = dct['dt']
            spare_amount = dct['spare_table']
    #the  basic settings are now loaded, nowfractal design define r4 black pearl to load enzymes and substrates
    spare_index = 0
    #creation of substrates
    substrates = []
    sub_cont = []
    sub_rep_table = {}
    sub_transform_dct = {} #this houses substrate ob_id-time pairs
    for dct in constants_container:
        if dct['MODULE_TYPE'] == 'substrate':
            sub_cont.append(dct)
    for dct in sub_cont:
        for i in range(0,dct['amount']):
            substrates.append(createSub(cell_radius, dct['type'], dct['mass'],dct['replenish']))
        sub_rep_table[dct['type']] = dct['replenish']
    
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
    
    #figure out pathway endpoints, make product dicts, these will be used to "store" products that can't react anymore.
    product_amounts = {}
    sub_types = []
    prod_types = []
    for dct in enz_cont:
        #find out the prod_types that have no sub_types to match
        if dct['sub_type'] not in sub_types:
            sub_types.append(dct['sub_type'])
        if dct['prod_type'] not in prod_types:
            prod_types.append(dct['prod_type'])
    for prod in prod_types:
        if prod not in sub_types:
            product_amounts[prod] = 0  
    #create substrate mass table
    sub_mass = {}
    for dct in sub_cont:
        sub_mass[dct['type']] = dct['mass']
    
    enz_mass = {}
    #should this be a dictionary with enzyme names and masses? YESH
    for enz in enzymes:
        if enz.name not in enz_mass:
            enz_mass[enz.name] = enz.obj.mass
    #create mobility tables for each particle
    sub_k_values = {}
    for key in sub_mass:
        rad = 0.066*sub_mass[key]**(1/3)*1e-9*2
        D = 310*1.38e-23/(3*0.7e-3*3.1415*rad)
        sub_k_values[key] = (2*D*dt)**(1/2)
    enz_k_values = {}
    for key in enz_mass:
        rad = 0.066*enz_mass[key]**(1/3)*1e-9
        D = 1.38e-23*310/(3*3.1415*1.0e-3*rad)
        enz_k_values[key] = (2*D*dt)**(1/2)
    
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
    
    #the lists for particle amounts
    sub_amounts = []
    for key in sub_k_values:
        list = []
        sub_amounts.append(list)
    step = 0
    #begin main loop
    react_ams = 0
    #final time list
    react_time_list = []
    while step < step_amount:
        #main loop goes here
        #update particle busynesses
        for en in enzymes:
            en.updBusy()
        for sub in substrates:
            sub.updBusy()
        k=0
        for sub in substrates:
            mass = sub.obj.mass
            dx = sub_movements[k][0][step%spare_amount]*sub_k_values[sub.type]
            dy = sub_movements[k][1][step%spare_amount]*sub_k_values[sub.type]
            x = sub.obj.position.x
            y = sub.obj.position.y
            if step == spare_amount:
                del sub_movements
                sub_movements = []
                for i in range(0,len(substrates)): 
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
            if step == spare_amount:
                del enz_movements
                enz_movements = []
                for i in range(0,len(enzymes)):
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
        #check and update bonding
        for enz in enzymes:
            if enz.status == 0:
                for sub in substrates:
                    if sub.status == 0 and sub.type == enz.sub_type:
                        bonded = 0
                        dist = math.hypot(enz.obj.position.x-sub.obj.position.x,enz.obj.position.y-sub.obj.position.y)
                        if dist < enz.react_range and enz.sub_type == sub.type :
                            bonded = transformsub(sub,enz, enz.react_chance,sub_mass[enz.prod_type],sub_rep_table[enz.prod_type])
                        if bonded > 0:
                            react_ams +=1
                            enz.status = enz.busy
                            sub.status = enz.busy
                            #check if substrate is of type
                            if sub_rep_table[enz.sub_type] == 1:
                                substrates.append(createSub(cell_radius, enz.sub_type, sub_mass[enz.sub_type],sub_rep_table[enz.sub_type]))
                                #create movements for this substrate...
                                movements_x = norm.rvs(size = spare_amount).tolist()
                                movements_y = norm.rvs(size = spare_amount).tolist()
                                mov = [movements_x,movements_y]
                                sub_movements.append(mov)
                            #check if substrate if of a type that needs not be simulated, then it can be removed from the
                            #substrate list and changed to just a number.
                            if sub.type == 2:
                                #create a new pair
                                sub_transform_dct[str(id(sub))] = 0
                            #if the substrate has transformed another time, make an entry to a list of times. Also delete this dict entry.
                            if sub.type == 3:
                                react_time_list.append(sub_transform_dct[str(id(sub))])
                                sub_transform_dct.pop(str(id(sub)))
                            if sub.type == 4:
                                sub_transform_dct.pop(str(id(sub)))
                            if sub.type in product_amounts:
                                product_amounts[sub.type] +=1
                                substrates.remove(sub)
                                sub_movements.pop()
                            break
        #collect data
        for i in range(0,len(sub_amounts)):
            a = 0
            for sub in substrates:
                if i == sub.type-1:
                    a += 1    
            if (i+1) in product_amounts:
                a += product_amounts[i+1] 
            sub_amounts[i].append(a)
        step += 1
        #print(id(substrates[1]))
        if step % 500 == 0 :
            if step % 1000 != 0:
                print("Step",step)
            if step % 1000 == 0:
                print("Step",step,",reactions/1000 steps:",react_ams)
                print("Different enzyme types:")
                print(sub_amounts[0][step-1],sub_amounts[1][step-1],sub_amounts[2][step-1],sub_amounts[3][step-1])
        #add one to the times in substrate dict
        for key in sub_transform_dct:
            sub_transform_dct[key] += 1
    cols = ['r','g','b','c','m','k','r']   
    time2 = tm.localtime()
    print("simulation took", tm.time()-time1,"seconds")
    print(react_time_list)
    #write simulation results to a file
    t_file = StringIO()
    for time in react_time_list:
        t_file.write(str(time)+',')
    t_file.seek(0,0)
    strfile = fio.writeOutput(sub_amounts)
    strfile.seek(0,0)
    filenlist = const_filename.split("/")
    filename = filenlist[len(filenlist)-2] + '-' +filenlist[len(filenlist)-1]
    t_filename = 'times'+filenlist[len(filenlist)-2] + '-' +filenlist[len(filenlist)-1]
    dat =  datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S-%f")
    outputfile = open("data/"+filename+dat+".txt",'w')
    for line in strfile:
        outputfile.write(line)
    t_outputfile = open("data/"+t_filename+dat+".txt",'w')
    for line in t_file:
        t_outputfile.write(line)
    strfile.close()
    outputfile.close()
    t_outputfile.close()

if __name__ == '__main__':
    main()
