'''
Created on Mar 20, 2015

@author: lipastomies
'''
import vector2

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
FREE = 1
BUSY = 0
ALIVE = 1
DEAD = 0
SUB_A = 1
SUB_B = 2
SUB_C = 3
ENZ_A = 1
ENZ_B = 2

class Obj(object):
    '''
    This class implements an object that resides in
    2d space. It has 1 vector, position. It also has mass and radius.
    I'll implement the random walk in another file.
    
    '''
    '''
    TODO:
    
    '''

    #def __init__(self, mass,radius, position):
    def __init__(self, mass, position):
        self.mass = float(mass)
        try:
            '''
            if float(radius)> 0:
                self.radius = float(radius)
            else :
                raise Exception("Radius not applicable!",radius)
            '''
            #the following three are vectors, see vektori.py
            self.position = position
        except:
            raise
        
    def setPosition(self,position):
        self.position = position
        
    def getPosition(self):
        return self.position
    
    def getMass(self):
        return self.mass
    
    #def getRadius(self):
    #    return self.radius
    
    def getDistance(self, toinen):
        yksi = self.getPosition()
        kaksi = toinen.getPosition()
        erotus = yksi - kaksi
        etaisyys = erotus.length()
        return etaisyys
    
    def __str__(self):
        string = "Mass: " + str(self.getMass()) + "\n"
        #string += "Radius: " + str(self.getRadius()) + "\n"
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
    Has state (busy, free)
    Has object for physics
    has type, to show which enzyme it is
    Methods that are needed:
    -check if busy, if busy, wait 1, then not busy
    -if not busy, check if possible to bind to substrates
    '''
    def __init__(self, obj, typ):
        self.obj = obj
        self.type = typ
        self.status = FREE

class Substrate(object):
    '''
    Implements an substrate-class
    Has object for physics
    has type, to show which substrate it is
    Methods that are needed:
    -transforming method, which destroys this substrate and spawns another, and makes the 
    '''
    def __init__(self, obj, typ):
        self.obj = obj
        self.type = typ
    
    def transform(self, typ):
        self.type = typ
                
    