import datetime

def SpecificTime(starttime, endtime, filename):
    lookup = "Start Time"
    with open(filename,'rb') as myFile:
        with open('temp.txt', 'w') as tempOutput:
            for line in myFile:
                if lookup.encode() in line:
                    tempOutput.write(line)
                elif line[0].isdigit():
                    lineList = line.split(',')
                    date = lineList[1]
                    #print(date)
                    time = lineList[2]
                    #print(time)
                    fulldate = ' '.join([date, time])
                    try:
                        linedatetime = datetime.datetime.strptime(fulldate, "%m/%d/%y %H:%M:%S")
                        if linedatetime > starttime:
                            if linedatetime < endtime:
                                tempOutput.write(line)
                    except:
                        linedatetime = datetime.datetime.strptime(fulldate, "%m/%d/%Y %H:%M:%S")
                        if linedatetime > starttime:
                            if linedatetime < endtime:
                                tempOutput.write(line)
