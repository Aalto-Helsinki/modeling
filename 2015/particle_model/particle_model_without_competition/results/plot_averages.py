import matplotlib.pyplot as plot
import sys

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
	substrate_1 = []
	substrate_2 = []
	product = []
	for fname in filenames:
		f = open(fname, 'r')
		lines = f.readlines()
		#for line in lines:
			#substrate.append(line.strip().strip(",").split(","))
		substrate_1.append(lines[0].strip().strip(",").split(","))
		substrate_2.append(lines[1].strip().strip(",").split(","))
		product.append(lines[2].strip().strip(",").split(","))
		f.close()
	#for line in file:
		#substrate.append(line.strip().split(","))
	colmap = ['g','b','r','y','c','m','k']
	#plot the averages
	for i in range(0,len(substrate_1)):
		substrate_1[i] = list(map(int,substrate_1[i]))
	for i in range(0,len(substrate_2)):
		substrate_2[i] = list(map(int,substrate_2[i]))
	for i in range(0,len(product)):
		product[i] = list(map(int,product[i]))
	
	averages = [[0]*len(substrate_1[0]),[0]*len(substrate_2[0]),[0]*len(product[0]) ]
	for i in range(0,len(substrate_1[0])):
		for subs in substrate_1:
			
			averages[0][i] += subs[i]
		averages[0][i] = averages[0][i]/len(substrate_1)
		#print(i)
	print("first subs made")
	for i in range(0,len(substrate_2[0])):
		for subs in substrate_2:
			#subs = list(map(int,subs))
			averages[1][i] += subs[i]
		averages[1][i] = averages[1][i]/len(substrate_2)
	print("second subs made")
	
	for i in range(0,len(product[0])):
		for subs in product:
			#subs = list(map(int,subs))
			averages[2][i] += subs[i]
		averages[2][i] = averages[2][i]/len(product)
	print("last subs made")
	plot.plot(averages[0],'g')
	
	plot.plot(averages[1],'r')
	
	plot.plot(averages[2],'b')
	'''
	for i in range(0, len(substrate)):
		substrate[i] = list(filter(None, substrate[i]))
		substrate[i] = list(map(int, substrate[i]))
		col = colmap[0]
		col = colmap[int(i%3)%len(colmap)]
		plot.plot(substrate[i],col)
	'''
	x_1 = int(0.6*(len(averages[2])))
	x_2 = len(averages[2])-1
	y_1 = averages[2][x_1]
	y_2 = averages[2][x_2]
	k = (y_2-y_1)/(x_2-x_1)
	print("the slope during the last 40% (60-100%) of the product curve:", k)
	plot.show()

if __name__ == "__main__":
	main()
