## -*- coding: utf-8 -*-
## BANANAPLOT.PY --  Plots SMPS data from TSI instruments using Aerosol Instrument Manager
##					 Extracts particle sizes, dN/dlogDp and time to create banana plots
##					 Saves processed data to DMA-MMDDYYYY-HHMM.txt
##					 
## Categories:
##		Aerosol nucleation
## Author:
##		Lee Tiszenkel, UAH

import matplotlib.pyplot as plt
import time
import sys
import numpy as np
import matplotlib.dates as mdates
import datetime #need datetime to create datetime variable type
import re
import os

def BananaPlot(filename):
    datastartline = 0
    ###This finds out the length of the header
    lookup = 'Start Time' #Column heading lines (first line of file we need)
    with open(filename, 'rb') as myFile:
        for num,line in enumerate(myFile, 1):
            if lookup.encode() in line:
                print('found at line:', num)
                dataStartLine = num-1

    ##This finds where the particle sizes are in the column header line
    y = np.genfromtxt(filename, skip_header=dataStartLine, comments='Comment', delimiter=',', max_rows=1) ##Grab column header line
    yy = [s for s in list(y) if str(s) != 'nan'] ##Every line in column header line aside from particle sizes is string and comes through as nan, so this checks
    tupleStart = list(y).index(yy[0]) ##Making our range of columns to grab Z
    tupleEnd = tupleStart + len(yy)
    Z=tuple(range(tupleStart,tupleEnd))
    y = np.array(yy) ##The last step made a list, so this converts it back to a numpy array for plotting
    
    #This grabs the full dn/dlogDPp array
    data = np.genfromtxt(filename, skip_header=dataStartLine+1, delimiter=',', usecols=Z)
    print(np.amax(data))
    dndlogdpMax = np.amax(data)
    
    #Take column indexes 1 and 2 (date, time)
    x = np.genfromtxt(filename, dtype=str, skip_header=dataStartLine+1, delimiter=',', usecols=(1,2))
    #Join the two columns together to make a %m/%d/%y %H:%M:%S format
    x = [' '.join(t) for t in x]
    #outFilename = 'LDMA' + re.sub('[:/ ]', '', x[0]) + '.txt'
    #print outFilename
    #Convert them from strings to datetime objects so we can use them to plot
    x = [datetime.datetime.strptime(t, "%m/%d/%y %H:%M:%S") for t in x]
    #x = [t + datetime.timedelta(hours=1) for t in x] ##Adds an hour for central/eastern conversion

    return x, y, data, dndlogdpMax
try:
	filename = sys.argv[1] #Takes the first command line argument after banana.py as the filename
except:
	print("No file supplied.\n")
	filename = input("Supply filename >")

#filename = DataManage()
#print filename
x,y,data,dndlogdpMax = BananaPlot(filename) ##Getting data from DataHarvest.py
#x2,y2 = SO2Data()

########################################
dndlogdpMax = 5000 #Max value of dN/dLogDp, comment out if you want max value to = max value in data, which may obfuscate features
########################################

colorticks = dndlogdpMax/4

#Creating a matplotlib figure, specifying size in inches
fig = plt.figure(figsize=(15,6))
ax = fig.add_subplot(2,1,1) #Putting the first plot 'ax' in the top position; eventually adding additional plots
#ax2 = fig.add_subplot(2,1,2)
ax.clear()

#Here it is, the meat of it: makes a contour plot, range of colors is from 0 to set max with steps of 500
#Extend keyword makes it so any value over set max is filled in with max color
bananaPlot = ax.contourf(x,y,data.T, np.arange(0, dndlogdpMax+1, 500), cmap='jet', extend='max')
#so2plot = ax2.plot(x2,y2)

#Formatting dates to a sane format
	#We have a MAJOR (Times) and a MINOR (dates)
	#myFmt corresponds to MINOR, myFmt2 to MAJOR
myFmt = mdates.DateFormatter("%m/%d/%Y") #Format date
myFmt2 = mdates.DateFormatter("%H:%M:%S") #Format time
myFmt3 = mdates.DateFormatter("%m/%d") #SO2 Format date
ax.xaxis.set_major_formatter(myFmt2)
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=int(((max(x)-min(x)).total_seconds())/5))) #6 marks on x axis
ax.xaxis.set_minor_formatter(myFmt)
ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
ax.xaxis.set_tick_params(which='minor', pad=15) #Keeps major/minor axis from overlapping

#Y axis needs to be logarithmic
ax.set_yscale('log')

#Colorbar Setup - putting neater ticks on, label
cb = fig.colorbar(bananaPlot, ax = ax, ticks = list(range(0,int(dndlogdpMax+1),int(colorticks))), extendrect=True)
cb.set_label('dN/dlogDp')

#Axis labels
ax.set_xlabel('Time (EDT)')
ax.set_ylabel('Dp (nm)')
ax.set_title('DMA: ' + str(min(x)) + ' - ' + str(max(x)) + ' (EDT)')

#Show plot
#plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
#plt.savefig('current.png', bbox_inches='tight', pad_inches=0)
plt.savefig('DMA' + time.strftime("%m%d%Y-%H%M") + '.png', bbox_inches='tight', pad_inches=0) #Saves to DMA-MMDDYYYY-HHMM.png
plt.show() #Show the plot. Comment this out if you just want to save it
