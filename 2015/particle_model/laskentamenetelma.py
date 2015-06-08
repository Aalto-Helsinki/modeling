'''
Created on Mar 28, 2015

@author: lipastomies
'''
import aurinkokunta
import vektori
import objekti

gravVakio = 6.67384e-11#gravity constant,
#will be changed to read it from a settings file 

def RK4(objekti,kunta,simulaatioaskel):
    '''
    Calculates the next position, velocity and acceleration of an object
    using 4th order Runge-Kutta method.
    Returns object's position, velocity and acceleration.
    '''
    '''
    NOTES:
    calculate the whole runge-kutta method for one object.
    The object's values should not be changed before all of the other 
    objects' values have been calculated.
    '''
    
    #calculate the coefficients
    
    #position and velocity of the object
    ob_pos = objekti.getPosition()
    ob_vel = objekti.getVelocity()
    
    #k_1_v, or the acceleration to the object in its place
    k_v1 = kiihtyvyysfunktio(ob_pos, kunta, kunta.getObjectIndex(objekti))
    #k_1_y, or the velocity of the object
    k_y1 = ob_vel
    #k_2_v, or the accel. to the object in a new place, using k_1_y
    k_v2_y1 =vektori.Vektori(0,0,0) + k_y1
    #k_v2_y1.scale(simulaatioaskel/2)
    k_v2_position = ob_pos + k_v2_y1.scale(simulaatioaskel/2)
    k_v2 = kiihtyvyysfunktio(k_v2_position, kunta, kunta.getObjectIndex(objekti))
    #k_2_y
    k_y2_v1 =vektori.Vektori(0,0,0) + k_v1
    k_y2 = ob_vel + k_y2_v1.scale(simulaatioaskel/2)
    #k_3_v
    k_v3_y2 =vektori.Vektori(0,0,0) + k_y2
    k_v3_position = ob_pos + k_v3_y2.scale(simulaatioaskel/2)
    k_v3 = kiihtyvyysfunktio(k_v3_position, kunta, kunta.getObjectIndex(objekti))
    #k_3_y
    k_y3_v2 =vektori.Vektori(0,0,0) + k_v2
    k_y3 = ob_vel + k_y3_v2.scale(simulaatioaskel/2)
    #k_4_v
    k_v4_y3 =vektori.Vektori(0,0,0) + k_y3
    k_v4_position = ob_pos + k_v4_y3.scale(simulaatioaskel)
    k_v4 = kiihtyvyysfunktio(k_v4_position, kunta, kunta.getObjectIndex(objekti))
    #k_4_y
    k_y4_v3 =vektori.Vektori(0,0,0) + k_v3
    k_y4 = ob_vel + k_y4_v3.scale(simulaatioaskel)
    #calculate velocity and position
    vel_temp = k_v1 + k_v2.scale(2) + k_v3.scale(2) + k_v4
    pos_temp = k_y1 + k_y2.scale(2) + k_y3.scale(2) + k_y4
    velocity = ob_vel + vel_temp.scale(simulaatioaskel/6)
    position = ob_pos + pos_temp.scale(simulaatioaskel/6)
    acceleration = kiihtyvyysfunktio(objekti.getPosition(), kunta, kunta.getObjectIndex(objekti))
    #returhn the object's position, velocity and acceleration
    return position,velocity,acceleration


def kiihtyvyysfunktio(paikka,kunta,indeksi):
    '''
    Calculates acceleration for the object in question.
    Iterates over the system, and ignores itself.
    Uses method kiihtyvyys.
    '''
    acc = vektori.Vektori(0,0,0)
    for kappale in kunta.objektilista:
        if kunta.objektilista[indeksi] != kappale:
            temp = kiihtyvyys(paikka, kappale)
            acc += temp
    
    return acc
    
def kiihtyvyys(paikka,objekti):
    '''
    Calculates the acceleration an object would experience
    in a place.
    This implementation is crucial for the RK4 method to work.
    Should only be called from kiihtyvyysfunktio.
    '''
    kiihtyvyys = vektori.Vektori(0,0,0)
    #get the vector for distance
    dist = objekti.getPosition()-paikka
    #get distance and masses of the objects
    etaisyys = dist.length()
    massa2 = objekti.getMass()
    #calculate the absolute value for force
    #calculate the unit vector for distance, since it is needed
    #scale the unit vector with the length of force
    abs_kiihtyvyys = gravVakio*massa2/(etaisyys*etaisyys)
    kiihtyvyys_suunta = dist.unitVector()
    return kiihtyvyys_suunta.scale(abs_kiihtyvyys)
    