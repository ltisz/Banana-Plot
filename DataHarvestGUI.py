## -*- coding: utf-8 -*-
## Author:
##		Lee Tiszenkel

import numpy as np #NumPy has genfromtxt, which we need
import datetime #need datetime to create datetime variable type
import re
import os
import sys

#Setting the path of the file to read to the same folder as the script
scriptdir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(scriptdir)

#Setting the filename
#try:
#	filename = sys.argv[1] #Takes the first command line argument after banana.py as the filename
#except:
#	print "No file supplied.\n"
#	filename = raw_input("Supply filename >")
	
##RETRIEVING DATA FROM FILE##
##x is the time
##y is the particle size
##data is the dN/dlogDp data

def BananaPlot():
    filename='temp.txt'
    datastartline = 0
    ###This finds out the length of the header
    lookup = 'Start Time' #Column heading lines (first line of file we need)
    with open(filename, 'rb') as myFile:
        for num,line in enumerate(myFile, 1):
            if lookup.encode() in line:
                print('found at line:', num)
                dataStartLine = num-1
    #with open(filename, 'rb') as myFile:
        
    ##This finds where the particle sizes are in the column header line
    y = np.genfromtxt(filename, skip_header=dataStartLine, comments='Comment', delimiter=',', max_rows=1) ##Grab column header line
    yy = [s for s in list(y) if str(s) != 'nan'] ##Every line in column header line aside from particle sizes is string and comes through as nan, so this checks
    tupleStart = list(y).index(yy[0]) ##Making our range of columns to grab Z
    tupleEnd = tupleStart + len(yy)
    Z=tuple(range(tupleStart,tupleEnd))
    y = np.array(yy) ##The last step made a list, so this converts it back to a numpy array for plotting
    #print y
    #Z = tuple(range(8,107)) #This will be the range of the columns to read, skipping colums that aren't relevant to the graph
    #The next line grabs just the particle sizes that the CPC measures:
    #It skips the header (18 lines), only grabs one row, and excludes the Comment line
    #y = np.genfromtxt(filename, skip_header=18, comments='Comment', max_rows=1, delimiter=',', usecols=Z)

    #This grabs the full dn/dlogDPp array
    data = np.genfromtxt(filename, skip_header=dataStartLine+1, delimiter=',', usecols=Z)
    print(np.amax(data))
    
    #Take column indexes 1 and 2 (date, time)
    x = np.genfromtxt(filename, dtype=str, skip_header=dataStartLine+1, delimiter=',', usecols=(1,2))
    #Join the two columns together to make a %m/%d/%y %H:%M:%S format
    x = [' '.join(t) for t in x]
    #outFilename = 'LDMA' + re.sub('[:/ ]', '', x[0]) + '.txt'
    #print outFilename
    #Convert them from strings to datetime objects so we can use them to plot
    try:
        x = [datetime.datetime.strptime(t, "%m/%d/%y %H:%M:%S") for t in x]
    except:
        x = [datetime.datetime.strptime(t, "%m/%d/%Y %H:%M:%S") for t in x]
    #x = [t - datetime.timedelta(hours=6) for t in x] #Subtracts 6 hours for UTC/CST conversion

    return x, y, data
