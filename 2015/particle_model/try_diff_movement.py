'''
A Quick-and-dirty test.
What to implement next:
-enzyme collision propability? is trivial, implemented
-enzyme business thingy, not implemented yet.
-no substrate can transform more than one time per timestep,
I think this can't happen now.
-more enzymes, adding them is quite easy now.
-REFACTORING!!!!!! this shit is atrocious. Put blocks of code in separate functions.
-multithreading, at least the iteration through subs and enzymes is possible. Perhaps a thread per enzyme? Then I really need the substrate business 
thingy, though.
as updating the placing. Nothing is dependent on others, really.
-Optimizing: vector calculations are better, don't know how to make them faster. Brownian movement is better now.
Perhaps this list could be, say, 1000 big, and when it is used, it would be called again. That would be efficient with almost no memory usage,
since it is only 2000 numbers wrapped in a list. Right?
'''

from vector2 import Vector2
import objects
from objects import Obj,Substrate,Enzyme
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.stats import norm
import matplotlib.pyplot as plot
import random
from builtins import range

ENZ_SUP = 999

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


def createEnz(cell_rad, type, mass):
    '''
    Creates an enzyme object that can then be appended to a list
    '''
    x = cell_rad +1
    y = cell_rad +1
    while (x*x + y*y) >= cell_rad*cell_rad:
        x = cell_rad*random.random()
        y = cell_rad*random.random()
    vec = Vector2(x,y)
    ob = Obj(mass,vec)
    return Enzyme(ob,type)


def createSub(cell_rad, type, mass):
    '''
    Creates a substrate object that can then be appended to a list.
    Perhaps the option to choose type is too much...
    '''
    x = cell_rad +1
    y = cell_rad +1
    while (x*x + y*y) >= cell_rad*cell_rad:
        x = cell_rad*random.random()
        y = cell_rad*random.random()
    vec = Vector2(x,y)
    ob = Obj(mass,vec)
    return Substrate(ob,type)


def main():
    '''
    '''
    #create lists for the enzymes to be
    enz = []
    subs = []
    product = []
    #constants
    #brownian motion
    dt = 1
    delta = 0.5
    time_range = 3000
    cell_rad = 10.0
    sub_count = 700
    enz_count = 10
    #enzyme propabilities of reaction
    
    #enz_a
    for s in range(1,enz_count):
        enz.append(createEnz(cell_rad, ENZ_SUP, 1))
        #enz.append(createEnz(10, objects.ENZ_B, 1))
    #try to make it a switch, whether a superenzyme or regular enzymes are used.
    for s in range(1,sub_count):
        subs.append(createSub(cell_rad, objects.SUB_A, 1))
    
    i=0
    sub_a_amount = []
    sub_b_amount = []
    sub_c_amount = []
    total = []
    sub_movements_x = []
    sub_movements_y = []
    #create all of the brownian movements beforehand, so that we only call rvs one time/object.
    for sub in subs:
        rands_x = norm.rvs(size = time_range,scale=delta**2*dt).tolist()
        rands_y = norm.rvs(size = time_range,scale=delta**2*dt).tolist()
        sub_movements_x.append(rands_x)
        sub_movements_y.append(rands_y)
    #brownian motion tables, so that if the indexed movement is not valid, a particle takes the values from here.
    #this lessens the amount of calling the norm function, which is costly
    add_table_x = norm.rvs(size = 5000,scale=delta**2*dt).tolist()
    add_table_y = norm.rvs(size = 5000,scale=delta**2*dt).tolist()
    add_index = 0
    while i < time_range:
        #updateobj(ea.obj, delta, dt)
        #updateobj(sub.obj, delta, dt)
        #for sub in subs:
            #updateobj(sub.obj, delta, dt)
        #move all of subs
        for sub in subs:
            dx = sub_movements_x[subs.index(sub)][i%time_range]
            dy = sub_movements_y[subs.index(sub)][i%time_range]
            x = sub.obj.position.x
            y = sub.obj.position.y
            
            while ((x+dx)**2 + (y+dy)**2) > cell_rad*cell_rad:
                dx = add_table_x[add_index%5000]
                dy = add_table_y[add_index%5000]
                add_index +=1
                #print((x+dx)**2 + (y+dy)**2)   
            if add_index == 5000:
                add_table_x = norm.rvs(size = 5000,scale=delta**2*dt).tolist()
                add_table_y = norm.rvs(size = 5000,scale=delta**2*dt).tolist()
                add_index =0
            dpos = Vector2(dx,dy)
            sub.obj.setPosition( sub.obj.getPosition() + dpos)
        for en in enz:
            updateobj(en.obj, delta, dt)
        
        for en in enz:
            for sub in subs:
                #if sub.type == en.type or en.type == ENZ_SUP:
                bonded=0
                if en.obj.getDistance(sub.obj) < 0.10 and sub.type is not objects.SUB_C:
                    bonded = transformsub(sub, 0.5)
                if bonded>0:
                    if sub.type == objects.SUB_C :
                        product.append(sub)
                        subs.remove(sub)
                    break
                        
        a = 0
        b = 0
        c = 0
        for sub in subs:
            if sub.type == objects.SUB_A:
                a += 1
            if sub.type == objects.SUB_B:
                b += 1
        for sub in product:
            c += 1
        sub_a_amount.append(a)
        sub_b_amount.append(b)
        sub_c_amount.append(c)
        total.append(a+b+c)
        i += 1
        if i % 10 == 0:
            print(i)
    
    plot.plot(sub_a_amount,'g')
    plot.plot(sub_b_amount,'r')
    plot.plot(sub_c_amount,'b')
    plot.plot(total,'k')
    plot.show()
    


if __name__ == '__main__':
    main()
