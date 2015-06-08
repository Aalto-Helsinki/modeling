'''
Created on Mar 20, 2015

@author: lipastomies
'''
import math


class Vector2(object):
    '''
    this class implements a two-dimensional vector.
    the vector has x,y components.
    You can scale vectors and sum them, as well as calculate their length
    '''
    '''
    
    '''


    def __init__(self, x,y):
        '''
        Constructor
        '''
        try:
            self.x=float(x)
            self.y=float(y)
        except ValueError:
            raise Vector2Exception("Could not initialize vector: One or more of initial values not of type float.",ValueError.__cause__)
    
    def __add__(self, right):
        v=Vector2(0,0)    
        v.x = self.x + right.x
        v.y = self.y + right.y
        return v
    
    def __sub__(self, right):
        v=Vector2(0,0)    
        v.x = self.x - right.x
        v.y = self.y - right.y
        return v
    

    
    def scale(self,value):
        vec = Vector2(self.getComponent("x")*value,self.getComponent("y")*value)
        return vec
    
    def getComponent(self,component):
        if component == 'x':
            return self.x
        if component == 'y':
            return self.y
        
    def addToComponent(self,component,value):
        if component == 'x':
            self.x += value
        elif component == 'y':
            self.y += value
            
    def length(self):
        length = 0.0
        length += self.x*self.x
        length += self.y*self.y
        return math.sqrt(length)
    
    def unitVector(self):
        #returns a unit vector with length of 1.
        #useful when only a direction is needed, e.g. when calculating a force
        length = self.length()
        unit_x = self.getComponent('x')/length
        unit_y = self.getComponent('y')/length
        return Vector2(unit_x,unit_y)
        
        
    def __str__(self):
        return str(self.getComponent('x')) + ' ' + str(self.getComponent('y')) 
    
    
class Vector2Exception(Exception):
    def __init__(self, description, data):
        self.description = description
        self.data = data

    