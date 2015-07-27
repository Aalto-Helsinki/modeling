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
        self.x=float(x)
        self.y=float(y)
        
    def __add__(self, right):   
        x = self.x + right.x
        y = self.y + right.y
        return Vector2(x,y)
    
    def __sub__(self, right):    
        x = self.x - right.x
        y = self.y - right.y
        return Vector2(x,y)
    

    
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
        x = self.x
        y = self.y
        length += x*x
        length += y*y
        return math.sqrt(length)
    
    def unitVector(self):
        #returns a unit vector with length of 1.
        #useful when only a direction is needed, e.g. when calculating a force
        length = self.length()
        if length <= 0:
            return Vector2(0,0)
        unit_x = self.getComponent('x')/length
        unit_y = self.getComponent('y')/length
        return Vector2(unit_x,unit_y)
        
        
    def __str__(self):
        return str(self.getComponent('x')) + ' ' + str(self.getComponent('y')) 
    
    
class Vector2Exception(Exception):
    def __init__(self, description, data):
        self.description = description
        self.data = data

    