'''
Created on Apr 14, 2015

@author: lipastomies
'''
from io import StringIO
#all of this is shiiitt
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
        delta = float(readnewline(file))
        enzyme_masses = readnewline(file).split(",")
        for e in enzyme_masses:
            e = float(e)
        sub_masses = readnewline(file).split(",")
        for s in sub_masses:
            s = float(s)
        enz_busyness = readnewline(file).split(",")
        for e in enz_busyness:
            e = int(e)
        enz_prob = readnewline(file).split(",")
        for e in enz_prob:
            e = float(e)
        enz_range = readnewline(file).split(",")
        for e in enz_range:
            e = float(e)
        sup_enz = int(readnewline(file))
        spare_table = int(readnewline(file))
        
        file.close()
        return {'radius':cell_rad,'enz_types':enz_types,'enz_amount_per_type':enz_am_per_type,'sub_amount':sub_amount,'steps':steps,
                'dt':dt,'delta':delta,'enz_mass':enzyme_masses,'sub_mass':sub_masses,'enz_busyness':enz_busyness,'enz_prob':enz_prob,
                'enz_range':enz_range,'if_sup_enz':sup_enz,'spare table':spare_table}

    
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
            for value in subs:
                file.write(string(value)+',')
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

class FileIOException(Exception):
    def __init__(self, description, data):
        self.description = description
        self.data = data