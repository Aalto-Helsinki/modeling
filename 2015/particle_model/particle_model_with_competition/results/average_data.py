import sys
from io import StringIO

def filterempties(string):
    if string == ' ' or string == '':
        return False
    return True
    
def main():
    '''
    This little script makes a plottable data file from the files that 
    are given as command line arguments. Also leaves out 99% of data, compressing and averaging it
    to make more beautiful and concise plots
    '''
    print("number of files to plot:",len(sys.argv[2:]))
    #colours = int(sys.argv[1])
    filenames = sys.argv[2:]
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
    printable = []
    for curve in averages:
        temp = []
        sm = 0
        for i in range(0,len(curve)):
            sm += curve[i]
            if i == 0:
                temp.append(curve[i])
            elif i%100 == 0:
                sm = sm / 100
                temp.append(sm)
                sm = 0
        printable.append(temp)
    for i in range(0,len(printable)):
        x_1 = int(0.6*(len(printable[i])))
        x_2 = len(printable[i])-1
        y_1 = printable[i][x_1]
        y_2 = printable[i][x_2]
        k = (y_2-y_1)/(x_2-x_1)
        print("the slope during the last 40% (60-100%) of the curve ",i,":", k)
    
    out = open(sys.argv[1],"w")
    for curve in printable:
        for value in curve:
            out.write(str(value)+',')
        out.write('\n')
    
    out.close()

if __name__ == "__main__":
    main()
