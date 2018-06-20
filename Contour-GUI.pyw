from Tkinter import *
from tkFileDialog    import askopenfilename
from datechecktest import SpecificTime
import datetime
import matplotlib.pyplot as plt
import time
from DataHarvestGUI import BananaPlot
import sys
import numpy as np
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *
from matplotlib.colors import LogNorm

def doNothing():
    print("Okay")
    
def openFile():
    #file_list=[]
    filename = askopenfilename(parent=root)
    file_list.insert(0, filename)
    T.insert('1.0', 'Loaded ' + filename + '\n')
    return filename

def dndlogdpMaxGet():
    T.insert(END, dndlogdpMax.get())

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def update_days():
    thirtydays = ['4','6','9','11']
    for mo in thirtydays:
        if monthStart.get() == mo:
            maxdays = 30
            print mo
            break
        elif monthStart.get() == '2':
            if is_leap_year(int(yearStart.get())):            
                maxdays = 29
            else:
                maxdays = 28
            print mo
            break
        else:
            maxdays = 31
            print mo
    dayStart.config(to=maxdays)
    
def update_days_end():
    thirtydays = ['4','6','9','11']
    for mo in thirtydays:
        if monthEnd.get() == mo:
            maxdays = 30
            print mo
            break
        elif monthEnd.get() == '2':
            if is_leap_year(int(yearEnd.get())):            
                maxdays = 29
            else:
                maxdays = 28
            print mo
            break
        else:
            maxdays = 31
            print mo
    dayEnd.config(to=maxdays)

def activateTime():
    spinboxes = [monthStart, yearStart, dayStart, hourStart, minuteStart, monthEnd, yearEnd, dayEnd, hourEnd, minuteEnd]
    print "activateTime"
    for box in spinboxes:
        box.config(state=NORMAL)
    timein()

def deactivateTime():
    spinboxes = [monthStart, yearStart, dayStart, hourStart, minuteStart, monthEnd, yearEnd, dayEnd, hourEnd, minuteEnd]
    print "deactivateTime"
    timeout()
    for box in spinboxes:
        box.config(state=DISABLED)
            
def timeout():
    monthStart.delete(0,"end")
    monthStart.insert(0,1)
    dayStart.delete(0,"end")
    dayStart.insert(0,1)
    yearStart.delete(0,"end")
    yearStart.insert(0,1900)
    hourStart.delete(0,"end")
    hourStart.insert(0,0)
    minuteStart.delete(0,"end")
    minuteStart.insert(0,0)
    monthEnd.delete(0,"end")
    monthEnd.insert(0,12)
    dayEnd.delete(0,"end")
    dayEnd.insert(0,31)
    yearEnd.delete(0,"end")
    yearEnd.insert(0,2200)
    hourEnd.delete(0,"end")
    hourEnd.insert(0,23)
    minuteEnd.delete(0,"end")
    minuteEnd.insert(0,59)

def timein():
    monthStart.delete(0,"end")
    monthStart.insert(0,datetime.datetime.now().month)
    dayStart.delete(0,"end")
    dayStart.insert(0,datetime.datetime.now().day)
    yearStart.delete(0,"end")
    yearStart.insert(0,datetime.datetime.now().year)
    hourStart.delete(0,"end")
    hourStart.insert(0,datetime.datetime.now().hour)
    minuteStart.delete(0,"end")
    minuteStart.insert(0,datetime.datetime.now().minute)
    monthEnd.delete(0,"end")
    monthEnd.insert(0,datetime.datetime.now().month)
    dayEnd.delete(0,"end")
    dayEnd.insert(0,datetime.datetime.now().day)
    yearEnd.delete(0,"end")
    yearEnd.insert(0,datetime.datetime.now().year)
    hourEnd.delete(0,"end")
    hourEnd.insert(0,datetime.datetime.now().hour)
    minuteEnd.delete(0,"end")
    minuteEnd.insert(0,datetime.datetime.now().minute)
    
def MakeBanana():
    fullstart = monthStart.get() + '/' + dayStart.get() + '/' + yearStart.get() + ' ' + hourStart.get() + ':' + minuteStart.get()
    fullend = monthEnd.get() + '/' + dayEnd.get() + '/' + yearEnd.get() + ' ' + hourEnd.get() + ':' + minuteEnd.get()
    #T.insert(END, fullend + ' ' + fullstart + '\n')
    starttime = datetime.datetime.strptime(fullstart, "%m/%d/%Y %H:%M")
    endtime = datetime.datetime.strptime(fullend, "%m/%d/%Y %H:%M")
    try:
        print starttime
        print endtime
        print file_list[0]
        SpecificTime(starttime, endtime, file_list[0])
    except:
        print "Error (no file loaded)"
        try:
            filename = askopenfilename(parent=root)
            SpecificTime(starttime, endtime, filename)
        except:
            print "Bad file."
    #try:
    MakeBananaPlot(dndlogdpMax.get())
    #except:
    #    print "Error making Banana Plot."

def MakeBananaPlot(dndlogdpMax):
    filename = 'temp.txt'
    #print filename
    x,y,data = BananaPlot() ##Getting data from DataHarvest.py
    #x2,y2 = SO2Data()
    #dndlogdpMax = 36000 #Max value of dN/dLogDp
    colorticks = dndlogdpMax/4

    #Creating a matplotlib figure, specifying size in inches
    fig = plt.figure(figsize=(8,3))
    ax = fig.add_subplot(2,1,1) #Putting the first plot 'ax' in the top position; eventually adding additional plots
    ax.clear()

    #Here it is, the meat of it: makes a contour plot, range of colors is from 0 to set max with steps of 500
    #Extend keyword makes it so any value over set max is filled in with max color
    bananaPlot = ax.contourf(x,y,data.T+0.1,500, cmap='jet', norm=LogNorm()) #extend='max')
    #np.arange(0, dndlogdpMax+1, 500),
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
    cb = fig.colorbar(bananaPlot, ax = ax)
    cb.set_label('dN/dlogDp')

    #Axis labels
    ax.set_xlabel('Time (UTC)')
    ax.set_ylabel('Dp (nm)')
    ax.set_title('NDMA: ' + str(min(x)) + ' - ' + str(max(x)) + ' (UTC)')
    plt.show()
    plt.savefig('NDMA' + time.strftime("%m%d%Y-%H%M") + '.png', bbox_inches='tight', pad_inches=0) #Saves to banana.png
    #fig.canvas.draw()

    #canvas = FigureCanvasTkAgg(fig, master=root)
    #plot_widget = canvas.get_tk_widget()

    #plot_widget.grid(row=8,columnspan=10)

    
file_list=[]
root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

#dndlogdpMax = IntVar(root)
# dndlogdpMax.set(32000)

# dndlogdpMaxMenuLabel=StringVar()
# dndlogdpMaxMenuLabel.set("Max dN/dLogDP")
# dndlogdpMaxMenuDir=Label(root, textvariable = dndlogdpMaxMenuLabel, height = 4)
# dndlogdpMaxMenuDir.grid(row=0, column=0, sticky=W)

#option = OptionMenu(root, dndlogdpMax, 48000, 72000, 88000, 104000, 120000, 136000, 152000)

# l = range(16000,2400000,16000)
# l = tuple(l)
# option = Spinbox(root, textvariable=dndlogdpMax, values=l)
# option.grid(row=0, column=1, sticky=W)
# option.delete(0,"end")
# option.insert(0,64000)

T = Text(root, height=2, width=50)
T.grid(row=0, column=2, columnspan=3)

radioBool = IntVar()
Radiobutton(root, text="Use entire file", variable=radioBool, value = 0, command=deactivateTime).grid(row=1,column=0)
Radiobutton(root, text="Select time range", variable=radioBool, value = 1, command=activateTime).grid(row=1,column=2)

starttimeLabel=StringVar()
starttimeLabel.set("Start Time: M/D/Y H:M")
starttimeDir=Label(root, textvariable=starttimeLabel, height=1)
starttimeDir.grid(row=2, column=0)

monthVarStart = IntVar(root)
dayVarStart = IntVar(root)
yearVarStart = IntVar(root)
hourVarStart = IntVar(root)
minuteVarStart = IntVar(root)
monthStart = Spinbox(root, from_=1, to=12, width=10, textvariable=monthVarStart, command=update_days, state=DISABLED)
monthStart.grid(row=3, column=0)
monthStart.delete(0,"end")
monthStart.insert(0,datetime.datetime.now().month)
dayStart = Spinbox(root, from_=1, to=31, width=10, textvariable=dayVarStart, state=DISABLED)
dayStart.grid(row=3, column=1)
dayStart.delete(0,"end")
dayStart.insert(0,datetime.datetime.now().day)
yearStart = Spinbox(root, from_=2000, to=2100, width=10, textvariable=yearVarStart, command=update_days, state=DISABLED)
yearStart.delete(0,"end")
yearStart.insert(0,datetime.datetime.now().year)
yearStart.grid(row=3, column=2)
hourStart = Spinbox(root, from_=0, to=23, width=10, textvariable=hourVarStart, state=DISABLED)
hourStart.grid(row=3, column=3)
minuteStart = Spinbox(root, from_=0, to=59, width=10, textvariable=minuteVarStart,state=DISABLED)
minuteStart.grid(row=3, column=4)

endtimeLabel=StringVar()
endtimeLabel.set("End Time: M/D/Y H:M")
endtimeDir=Label(root, textvariable=endtimeLabel, height=1)
endtimeDir.grid(row=4, column=0)

monthVarEnd = IntVar(root)
dayVarEnd = IntVar(root)
yearVarEnd = IntVar(root)
hourVarEnd = IntVar(root)
minuteVarEnd = IntVar(root)
monthEnd = Spinbox(root, from_=1, to=12, width=10, textvariable=monthVarEnd, command=update_days_end,state=DISABLED)
monthEnd.grid(row=5, column=0)
monthEnd.delete(0,"end")
monthEnd.insert(0,datetime.datetime.now().month)
dayEnd = Spinbox(root, from_=1, to=31, width=10, textvariable=dayVarEnd,state=DISABLED)
dayEnd.grid(row=5, column=1)
dayEnd.delete(0,"end")
dayEnd.insert(0,datetime.datetime.now().day)
yearEnd = Spinbox(root, from_=2010, to=2100, width=10, textvariable=yearVarEnd, command=update_days_end,state=DISABLED)
yearEnd.grid(row=5, column=2)
yearEnd.delete(0,"end")
yearEnd.insert(0,datetime.datetime.now().year)
hourEnd = Spinbox(root, from_=0, to=23, width=10, textvariable=hourVarEnd,state=DISABLED)
hourEnd.grid(row=5, column=3)
minuteEnd = Spinbox(root, from_=0, to=59, width=10, textvariable=minuteVarEnd,state=DISABLED)
minuteEnd.grid(row=5, column=4)

yearVarStart.set(1900)
monthVarStart.set(1)
dayVarStart.set(1)
hourVarStart.set(0)
minuteVarStart.set(0)
yearVarEnd.set(2200)
monthVarEnd.set(12)
dayVarStart.set(31)
minuteVarStart.set(59)
hourVarStart.set(23)

button = Button(root, text="Make Banana Plot", command = MakeBanana)
button.grid(row=7,columnspan=3)

root.config(menu=menubar)
root.mainloop()
