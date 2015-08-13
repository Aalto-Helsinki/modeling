'''
Created on Mar 20, 2015

@author: lipastomies
'''
import vector2
import math

'''
This file implements the classes object, enzyme and
substrate, which have the following properties:
-object:
    has mass, radius, position
-enzymes and substrates:
-contain an object
-have types

-substrates can spawn new substrates when they die
-enzymes can transform substrates when they interact with them
-random walking is the name of the game 
-the physics are not considered here
'''

class Obj(object):
    '''
    This class implements an object that resides in
    2d space. It has 1 vector, position. It also has mass and radius.
    I'll implement the random walk in another file.
    '''

    '''
    TODO:
    
    '''
    def __init__(self, mass, position):
        try:
            #the following is a vector, see vector2.py
            self.position = position
            self.mass = float(mass)
        except:
            raise
        
    def setPosition(self,position):
        self.position = position
        
    def getPosition(self):
        return self.position
    
    def getMass(self):
        return self.mass
    
    def getDistance(self, toinen):
        return math.hypot(toinen.position.x-self.position.x,toinen.position.y-self.position.y)
    
    def __str__(self):
        string = "Mass: " + str(self.getMass()) + "\n"
        string += "Position: " + str(self.getPosition()) + "\n"
        return string
    
    def plot(self):
        '''
        This method is used to print the position of an object
        '''
        string = str(self.position)
        return string
        
class Enzyme(object):
    '''
    Implements an enzyme-class
    Has state
    Has object for physics
    Has the type of the substrate it processes
    Has type of the product it produces
    Methods that are needed:
    Busyness method
    -check if busy, if busy, wait, 
    -if not busy, check if possible to bind to substrates
    Transform a substrate to the new type (the product type)
    '''
    def __init__(self,name, obj, sub_type, prod_type,group_id,r_chance,r_range,busy):
        self.obj = obj
        self.sub_type = sub_type
        self.prod_type = prod_type
        self.group_id = group_id
        self.react_chance = r_chance
        self.react_range = r_range
        self.name = name
        self.busy = busy
        self.status = 0

    def updBusy(self):
        if self.status > 0:
            self.status -= 1
            
    def transformSub(self,sub):
        '''
        Transforms a substrate involved in a reaction. If the substrate is not
        of the right type, nothing happens.
        '''
        if sub.type == self.sub_type:
            sub.type = self.prod_type
        

class Substrate(object):
    '''
    This class implements a substrate object, that can then be used for
    simulating substrate and enzyme interactions.
    '''
    def __init__(self, obj, typ, rep):
        self.obj = obj
        self.type = typ
        self.replenish = rep
        self.status = 0
    
    def transform(self, typ, new_mass,new_replenish):
        self.type = typ
        self.obj.mass = new_mass
        self.replenish = new_replenish
    
    def updBusy(self):
        if self.status > 0:
            self.status -= 1
