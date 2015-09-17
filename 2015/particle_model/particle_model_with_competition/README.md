
README

The synergy model is constructed from vector2.py, objects.py, fileio.py and finally simulate.py, the main simulation file for the model.
The model runs on python version 3, tested with python 3.4.3.
The model is a command line tool, meaning that it has no real UI.
The usage of the model is simple: First, create a setting file for your simulation, that has the proper attributes for your preferred simulation.
A working example file can be found in the settings folder. In this file, the user can define the simulation constraints as well as the simulated enzymes
and substrates.
After this, the model is run by giving it the setting file as an argument. An example command line call is as follows:

python3 simulate.py name_of_settings_file

After this, the model simulates the scenario and in the end spews the data files in the data folder.
The data file contains the amounts of different substrates at different points of time.
This can be changed if one is adept in python. 
The results folder contains a few ready-made scripts for making sense of the data.
