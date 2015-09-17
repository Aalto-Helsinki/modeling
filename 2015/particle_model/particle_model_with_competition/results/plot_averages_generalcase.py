import matplotlib.pyplot as plot
import sys

def filterempties(string):
	if string == ' ' or string == '':
		return False
	return True

def main():
	'''
	This little script prints out the propane time evolution from the files that 
	are given as command line arguments (for example command "python plot.py data/no_*"
	chooses all of the files beginning with "no_", so all of the files with enzymes as separate.
	
	'''
	print("number of files to plot:",len(sys.argv[1:]))
	#colours = int(sys.argv[1])
	filenames = sys.argv[1:]
	#print(filenames)
	#filename =  sys.argv[1]
	#file = open(filename, 'r')
	substrates = []
	for fname in filenames:
		f = open(fname, 'r')
		lines = f.readlines()
		for line in lines:
			llist = line.strip("\n").strip(",").split(',')
			llist = list(filter(filterempties,llist))
			substrates.append(list(map(float, llist ) ) )
		f.close()
	curvenum = int(len(substrates)/len(filenames))
	averages = []
	print("number of curves:",curvenum)
	for i in range(0,curvenum):
		all_of_the_relevant_curves = []
		curve = []
		for j in range(0,len(substrates) ):
			if (j+ (curvenum-i)) % curvenum == 0:
				all_of_the_relevant_curves.append(substrates[j])
		for index in range(0, len(substrates[0]) ):
			average = 0
			for lst in all_of_the_relevant_curves:
				average += lst[index]
			average = average / len(all_of_the_relevant_curves)
			curve.append(average)
		averages.append(curve)
	colmap = ['g','b','r','y','c','m','k']
	#plot the averages
	for curve in averages:
		plot.plot(curve,colmap[averages.index(curve)])
	plot.show()

if __name__ == "__main__":
	main()
