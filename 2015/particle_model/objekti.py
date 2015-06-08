'''
Created on Mar 20, 2015

@author: lipastomies
'''
import vektori

class Objekti(object):
    '''
    This class implements an object that resides in
    3d space. It has 3 vectors, acceleration, position and velocity. It also has mass and radius.
    The physics of objects are not considered in this class.
    
    '''
    '''
    TODO:
    
    '''


    def __init__(self, mass,r, position,velocity,acceleration,name):
        self.mass = float(mass)
        try:
            if float(r)> 0:
                self.radius = float(r)
            else :
                raise Exception("Radius not applicable!",r)
            #the following three are vectors, see vektori.py
            self.position = position
            self.velocity = velocity
            self.acceleration = acceleration
            self.name = name
        except:
            raise
        
    def setPosition(self,position):
        self.position = position
    
    def setVelocity(self, velocity):
        self.velocity = velocity
        
    def setAcceleration(self,acceleration):
        self.acceleration = acceleration
        
    def getPosition(self):
        return self.position
    
    def getVelocity(self):
        return self.velocity
    
    def getAcceleration(self):
        return self.acceleration
    
    def getMass(self):
        return self.mass
    
    def getName(self):
        return self.name
    
    def getRadius(self):
        return self.radius
    
    def getDistance(self, toinen):
        yksi = self.getPosition()
        kaksi = toinen.getPosition()
        erotus = yksi - kaksi
        etaisyys = erotus.length()
        return etaisyys
    
    def __str__(self):
        string = "Object name: " + self.name +"\n" + "Mass: " + str(self.getMass()) + "\n"
        string += "Radius: " + str(self.getRadius()) + "\n"
        string += "Position: " + str(self.getPosition()) + "\n"
        string += "Velocity: " + str(self.getVelocity()) + "\n"
        string += "Acceleration: " + str(self.getAcceleration()) + "\n"
        return string
    
    def plot(self):
        '''
        This method is used to print the position of an object
        '''
        string = str(self.position)
        return string
        