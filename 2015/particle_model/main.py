'''
A Quick-and-dirty test.
What to implement next:
-enzyme business thingy, stop evaluating the sub list when enzyme and sub bind, done.
-no substrate can transform more than one time per timestep, this can happen, just not to the same enzyme. Hwo to get around this? a "business"-marker for
substrates, too?
-No enzyme can bond to more than one substrate at a time, that is done now.
-move propane to a different list, so that we don't need to iterate over it.
Then, in the end of the simulation this might be substantial. 
Implemented
-more enzymes. Adding them is easy.
-REFACTORING!!!!!! this shit is atrocious
    But how? more functions, that much is obvious.

-Are there faster methods? Code vectorization?
-multithreading, at least the iteration through subs and enzymes is possible, as well
as updating the placing. Nothing is dependent on others, really.
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


def updateobj(obj, delta, dt):
    x = obj.getPosition().getComponent("x")
    y = obj.getPosition().getComponent("y")
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
    if random.random() > a:
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
    Create lists of enzymes and substrates
    make them walk randomly
    plot movements
    '''
    #create lists for the enzymes to be
    enz = []
    subs = []
    product = []
    #constants
    #brownian motion
    dt = 1
    delta = 0.5
    #enzyme propabilities of reaction
    
    #enz_a
    for s in range(1,5):
        enz.append(createEnz(10, objects.ENZ_A, 1))
        enz.append(createEnz(10, objects.ENZ_B, 1))
    #vec = Vector2(2,3)
    #ob = Obj(1,vec)
    #sub = Substrate(ob,1)
    #spawn substrates and enzymes, first 1 enzyme and 10 substrates
    for s in range(1,750):
        subs.append(createSub(10, objects.SUB_A, 1))
    
    i=0
    sub_a_amount = []
    sub_b_amount = []
    sub_c_amount = []
    total = []
    while i < 1000:
        #updateobj(ea.obj, delta, dt)
        #updateobj(sub.obj, delta, dt)
        for sub in subs:
            updateobj(sub.obj, delta, dt)
        for en in enz:
            updateobj(en.obj, delta, dt)
        #if ea.obj.getDistance(sub.obj) < 0.5:
        #   sub.transform(objects.SUB_B)
        #    print("Reaction happened @",i)
        #substrate
        #print(ea.obj.plot())
        
        for ea in enz:
            #switch for not checking subs if one has already bonded 
            bonded=0
            for sub in subs:
                #stop if bonding happens
                if sub.type == ea.type:
                    if ea.obj.getDistance(sub.obj) < 0.15:
                        bonded = transformsub(sub, 0.75)
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
            c +=1
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
    #plot.show()

    


if __name__ == '__main__':
    main()