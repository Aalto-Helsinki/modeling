'''
Created on Apr 14, 2015

@author: lipastomies
'''
import aurinkokunta
import objekti
import vektori
import simulaatio

class FileIO(object):
    '''
    This class has the necessary functions that are needed for loading simulation data from files,
    as well as loading initial data that the program uses for initialization.
    The files used will have human-readable formatting, for ease of use.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def loadSystem(self,file):
        '''
        Loads a planetary system from file.
        Returns a complete planetary system.
        '''
        kunta = aurinkokunta.Aurinkokunta()
        #add exception handling   
        #loop to check the block, if the string is empty,
        #EOF has appeared
        current_line = readnewline(file)
        while current_line != '':
            if current_line.startswith("#Planeetta") : #if the block starts with #Planeetta
                listoflines = []
                current_line = readnewline(file)
                while current_line.startswith("#") == False:#reached the end of a block
                    listoflines.append(current_line)
                    current_line = readnewline(file)
                    if current_line == '':
                        break
                #self.loadplanet(listoflines)
                try:
                    planet =  self.loadplanet(listoflines)
                    kunta.addObject(planet)
                except:
                    raise
                #send listoflines to a function that extracts the data in it
                #create a new planet
                #add planet to solar system
            elif current_line.startswith("#Planeetta") == False and current_line.startswith("#") == True:#another block
                current_line = readnewline(file)
                while current_line.startswith("#") == False:
                    current_line = readnewline(file)
            else :#if line starts with something other than a block
                current_line = readnewline(file)
                
        return kunta
    
    def loadplanet(self, listoflines):
        '''
        Loads a planet from a list of strings.
        Returns an object
        '''
        
        #read the name
        i=0
        if listoflines[i].strip().startswith("Nimi"):
            name = listoflines[i].split(":")[1].strip()
            i +=1
        else :
            raise FileIOException("Name of planet not found!",listoflines[i])
        #read the mass
        if listoflines[i].strip().startswith("Massa"):
            mass = float(listoflines[i].split(":")[1].strip())
            i+=1
        else:
            raise FileIOException("Mass of planet not found!",listoflines[i])
        #read the radius
        if listoflines[i].strip().startswith("Sade"):
            radius = float(listoflines[i].split(":")[1].strip())
            i+=1
        else:
            raise FileIOException("radius of planet not found!",listoflines[i])
        
        try:
            if listoflines[i].strip().startswith("Paikka"):
                pos = self.loadvector(listoflines[i])
                i+=1
            else :
                raise FileIOException("Could not find position vector descriptor",listoflines[i])
        except FileIOException:
            raise 
        #read speed
        try:
            if listoflines[i].strip().startswith("Nopeus"):
                vel = self.loadvector(listoflines[i])
                i+=1
            else :
                raise FileIOException("Could not find velocity vector descriptor",listoflines[i])
        except FileIOException:
            raise
        #read acceleration
        try:
            if listoflines[i].strip().startswith("Kiihtyvyys"):
                acc = self.loadvector(listoflines[i])
            else :
                raise FileIOException("Could not find acceleration vector descriptor",listoflines[i])
        except FileIOException:
            raise 
        #create object
        obj = objekti.Objekti(mass,radius,pos,vel,acc,name)
        return obj
    
    def loadvector(self,line):
        values = list(filter(None, line.strip().split(":")[1].split(" ")))
        if len(values) != 3:
            raise FileIOException("Position vector hasn't got 3 members!",line)
        vect = vektori.Vektori(values[0],values[1],values[2])
        return vect
    
    def loadSimulation(self, listoflines): 
        '''
        Loads simulation variables:
        Start, end, step.
        '''
        i=0
        
        #start
        if listoflines[i].strip().startswith("Alku"):
            start = float(listoflines[i].split(":")[1].strip())
        #end
        i += 1
        if listoflines[i].strip().startswith("Loppu"):
            end = float(listoflines[i].split(":")[1].strip())
        #step
        i += 1 
        if listoflines[i].strip().startswith("Vali"):
            step = float(listoflines[i].split(":")[1].strip())
        ret = simulaatio.Simulaatio(step)
        ret.setEnd(end)
        ret.setStart(start)
        return ret
        #return a simulation
    
    
    def saveSystem(self, system, file):
        '''
        Saves a planetary system to a file specified by the user.
        '''
        
        for kappale in system.objektilista:
            file.write("#Planeetta\n")
            file.write("Nimi: " + kappale.getName()+"\n")
            file.write("Massa: " + str(kappale.getMass())+"\n")
            file.write("Sade: " + str(kappale.getRadius())+"\n")
            file.write("Paikka: " + str(kappale.getPosition())+"\n")
            file.write("Nopeus: " + str(kappale.getVelocity())+"\n")
            file.write("Kiihtyvyys: " + str(kappale.getAcceleration())+"\n")
            file.write("\n")
    
def readnewline(file):
    '''
    A function to read a new line. It continues to read the 
    new lines if it comes across a comment.
    Therefore, it ignores comments.
    Also ignores whitespace.
    '''
    current_line = file.readline().strip(" ")
    while current_line.startswith("//") or current_line == "\n":
        current_line = file.readline().strip(" ")
    return current_line

class FileIOException(Exception):
    def __init__(self, description, data):
        self.description = description
        self.data = data