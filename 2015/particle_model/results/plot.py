import matplotlib.pyplot as plot
import sys

def main():
	'''
	This little script prints out the propane time evolution from the files that 
	are given as command line arguments (for example command "python plot.py data/no_*"
	chooses all of the files beginning with "no_", so all of the files with enzymes as separate.
	
	'''
	print(len(sys.argv))
	colours = int(sys.argv[1])
	filenames = sys.argv[2:]
	print(filenames)
	#filename =  sys.argv[1]
	#file = open(filename, 'r')
	substrate = []	
	for fname in filenames:
		f = open(fname, 'r')
		lines = f.readlines()
		substrate.append(lines[2].strip().strip(",").split(","))	
		f.close()
	#for line in file:
		#substrate.append(line.strip().split(",")) 	
	colmap = ['g','b','r','y','c','m','k']	
	for i in range(0, len(substrate)):
		substrate[i] = list(filter(None, substrate[i]))
		substrate[i] = list(map(int, substrate[i]))
		col = colmap[0]		
		col = colmap[int(i/colours)%len(colmap)]
		plot.plot(substrate[i],col)	
	plot.show()

if __name__ == "__main__":
	main()