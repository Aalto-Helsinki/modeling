How to use the results
----------------------
This folder contains the parameter scans made with particle model.
These parameter scans are in folders. each folder has many files,
with appropriate names that tell if the file 
1)has "superenzyme"/scaffolding enabled
2)has certain parameters for the scan.
Every file contains the amounts of different substrates in its lines.
Each substrate has one line, and different values are separated by commas.
The file plot.py is an example file to show how You can load and visualize 
the data in the datafiles.
----------------------
About plot.py
----------------------
plot.py needs matplotlib for it to function.
It works on linux and perhaps on windows.
It takes as its arguments the names of the files
you want to visualize, and draws plots of the propane
concentrations. It also colors the lines (it colors 10 lines
with the same color, and then changes the color).
----------------------