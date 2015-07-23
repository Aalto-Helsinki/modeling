'''
Created on Apr 14, 2015

@author: lipastomies
'''
from io import StringIO
#all of this is shiiitt
class fileIO(object):
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
        
    def loadSettings(self, filename):
        '''
        Loads the settings for simulation from a file called, say,
        "config" or something, this can be passed as an argument for the program file that is used.
        
        Returns an ensemble of settings, we'll see what is the easiest way for us.
        A dictionary is quite easy, since it allows for us to have named values.
        Let's go with a dict. Dear god that's horrifying.
        '''
        file = open(filename,'r')
        rets = 0
        cell_rad = float(readnewline(file))
        enz_types = int(readnewline(file))
        enz_am_per_type = int(readnewline(file))
        sub_amount = int(readnewline(file))
        steps = int(readnewline(file))
        dt = float(readnewline(file))
        replenish = float(readnewline(file))
        if replenish < 1:
            replenish = 0
        else:
            replenish = 1
        enz_masses = readnewline(file).strip().split(",")
        enz_masses = list(map(float,enz_masses))
        sub_masses = readnewline(file).strip().split(",")
        sub_masses = list(map(float,sub_masses))
        enz_busyness = readnewline(file).strip().split(",")
        enz_busyness = list(map(int,enz_busyness))
        enz_prob = readnewline(file).strip().split(",")
        enz_prob = list(map(float,enz_prob))
        enz_range = readnewline(file).strip().split(",")
        enz_range = list(map(float,enz_range))
        sup_enz = int(readnewline(file))
        spare_table = int(readnewline(file))
        
        file.close()
        return {'radius':cell_rad,'enz_types':enz_types,'enz_amount_per_type':enz_am_per_type,'sub_amount':sub_amount,'steps':steps,
                'dt':dt,'replenish':replenish,'enz_mass':enz_masses,'sub_mass':sub_masses,'enz_busy':enz_busyness,'enz_prob':enz_prob,
                'enz_range':enz_range,'if_sup_enz':sup_enz,'spare_table':spare_table}
    
    def loadEnzyme(self,listoflines):
        pass
    
    def loadSubstrate(self,listoflines):
        pass
    
    def altLoadSettings(self, listoflines):
        pass
    
    def loadFile(self,filename):
        pass
    

    
    def writeOutput(self,results):
        '''
        Write the list containing simulation data to a
        file, so that it can be loaded with matlab/matplotlib/other applications
        returns a stringIO object.
        '''
        '''
        Writes the substrate concentrations as comma-separated rows,
        with each row meaning one substrate.
        '''
        file = StringIO()
        for sub in results:
            for value in sub:
                file.write(str(value)+',')
            file.write('\n')
        return file
    
    
def readnewline(file):
    '''
    A function to read a new line. It continues to read the 
    new lines if it comes across a comment.
    Therefore, it ignores comments.
    Also ignores whitespace.
    '''
    current_line = file.readline().strip(" ")
    while current_line.startswith("//") or current_line == "\n" or current_line.startswith("#"):
        current_line = file.readline().strip(" ")
    return current_line

class fileIOException(Exception):
    def __init__(self, description, data):
        self.description = description
        self.data = data