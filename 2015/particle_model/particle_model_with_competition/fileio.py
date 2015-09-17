'''
Created on Jul 14, 2015
@author: Arto Lehisto
'''
from io import StringIO

class fileIO(object):
    '''
    This class has the necessary functions that are needed for loading simulation data from files,
    as well as loading initial data that the program uses for initialization.
    The files used have human-readable formatting, for ease of use.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def loadSettings(self, filename):
        '''
        DEPRECATED
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
        '''
		This method assumes that it has been 
		passed a settings file module
		from the method readmodule or something 
		similar, i.e. it starts with a line like 
		#Module: asd
		and ends with a line #Module:End
		If the module does not respect
		these rules, it is discarded and an exception is raised.
		The lines it gets are already cleaned with readnewline()
		The method returns a dict containing all of the values
		needed to spawn a list of enzymes in the simulation.
		'''
        values = {}
        #gather all of the values in a dictionary
        for i in range(0,len(listoflines)) : #-1 for the module:end
            current_line = listoflines[i]
            linelist = current_line.strip("\n").split(":")
            values[linelist[0].strip()] = linelist[1].strip()
            #use that dictionary for loading the values in our enzyme dict
        enz_dict = {}
        try:
            enz_dict['name'] = values['name']
            enz_dict['mass'] = float(values['mass'])
            enz_dict['amount'] = int(values['amount'])
            enz_dict['sub_type'] = int(values['sub_type'])
            enz_dict['prod_type'] = int(values['prod_type'])
            enz_dict['reaction_chance'] = float(values['reaction_chance'])
            enz_dict['reaction_range'] = float(values['reaction_range'])
            enz_dict['group_id'] = int(values['group_id'])
            enz_dict['busy'] = int(values['busy'])
            enz_dict['MODULE_TYPE'] = 'enzyme'
        except:
            raise
        return enz_dict
    
    def loadSubstrate(self,listoflines):
        '''
        This method assumes that it has been 
        passed a settings file module
        from the method readmodule or something 
        similar, i.e. it starts with a line like 
        #Module: asd
        and ends with a line #Module:End
        If the module does not respect
        these rules, it is discarded and an exception is raised.
        The lines it gets are already cleaned with readnewline()
        The method returns a dict containing all of the values
        needed to spawn a list of substrates in the simulation.
        '''
        values = {}
        #gather all of the values in a dictionary
        for i in range(0,len(listoflines)) : #-1 for the module:end
            current_line = listoflines[i]
            linelist = current_line.strip("\n").split(":")
            values[linelist[0].strip()] = linelist[1].strip()
        #use that dictionary for loading the values in our enzyme dict
        try:
            sub_dict = {}
            sub_dict['mass'] = float(values['mass'])
            sub_dict['amount'] = int(values['amount'])
            sub_dict['type'] = int(values['type'])
            sub_dict['replenish'] = int(values['replenish'])
            sub_dict['MODULE_TYPE'] = 'substrate'
        except:
            raise
        return sub_dict

    def altLoadSettings(self, listoflines):
        '''
        This method assumes that it has been 
        passed a settings file module
        from the method readmodule or something 
        similar, i.e. it starts with a line like 
        #Module: asd
        and ends with a line #Module:End
        If the module does not respect
        these rules, it is discarded and an exception is raised.
        The lines it gets are already cleaned with readnewline()
        The method returns a dict containing all of the values
        needed to load settings in the simulation.
        '''
        values = {}
        #gather all of the values in a dictionary
        for i in range(0,len(listoflines)) : #-1 for the module:end
            current_line = listoflines[i]
            linelist = current_line.strip("\n").split(":")
            values[linelist[0].strip()] = linelist[1].strip()
        #use that dictionary for loading the values in our enzyme dict
        try:
            set_dict = {}
            set_dict['cell_rad'] = float(values['cell_rad'])
            set_dict['step_amount'] = int(values['step_amount'])
            set_dict['dt'] = float(values['dt'])
            set_dict['spare_table'] = int(values['spare_table'])
            set_dict['MODULE_TYPE'] = 'settings'
        except:
            raise
        return set_dict

    def loadFile(self,filename):
        '''
        This method returns a list of dictionaries
        containing the variables needed for the rettings
        and enzymes, as well as substrates.
        '''
        #if settings are loaded, how many substrates and enzymes are loaded
        f = open(filename,"r")
        current_line = readnewline(f)
        
        #the container for blocks, a list of dictionaries
        container = []
        while current_line != '':
            if current_line.startswith("#Module"):
                listoflines = []
                while current_line != '':
                    listoflines.append(current_line)
                    if current_line.startswith("#"):
                        if current_line.split(":")[1].strip().startswith("End"):
                            break
                    current_line = readnewline(f)
                module = self.chooseModule(listoflines)
                container.append(module)
            current_line = readnewline(f)
        f.close()
        return container
    
    def chooseModule(self, listoflines):
        '''
        This method decides which module the coming listoflines
        is and sends it to the right function.
        '''
        var = listoflines[0].split(":")[1].strip()
        if var == "Settings":
            return self.altLoadSettings(listoflines)
        elif var == "Enzyme":
            return self.loadEnzyme(listoflines)
        elif var == "Substrate":
            return self.loadSubstrate(listoflines)
    
    
    def writeOutput(self,results):
        '''
        Write the list containing simulation data to a
        file, so that it can be loaded with matlab/matplotlib/other applications
        returns a stringIO object.
        '''
        f = StringIO()
        for sub in results:
            for value in sub:
                f.write(str(value)+',')
            f.write('\n')
        return f
    
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

class fileIOException(Exception):
    def __init__(self, description, data):
        self.description = description
        self.data = data
