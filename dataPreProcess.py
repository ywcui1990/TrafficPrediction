import pandas as pd 
import numpy as np
from pandas import DataFrame, Series
import csv

import matplotlib.pyplot as plt

from pylab import *
if isinteractive() is not True:
  ion()

# fileName = 'data/New_York_VOL_2011.csv'
fileName = 'data/VOL_2011.csv'
csvfile = open(fileName)
csvreader = csv.reader(csvfile, delimiter=',')
headline = csvreader.next()
csvfile.close()

print " Read in data "
# parse date while reading the data
dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M')
df = pd.read_csv(fileName, parse_dates=['Start_Time'], date_parser=dateparse)
# df = pd.read_csv(fileName)

# print " Convert to datetime type"
# df['Start_Time'] = pd.to_datetime(df['Start_Time'])

stationList = pd.unique(df['RCStation'])

# extract day of the year 
f = lambda x: x.dayofyear




# calculate number of days and data points per monitoring station
dataPerStation = []
numDayPerStation = []

for station in stationList:
	
	dfSelect = df[df['RCStation']==station]
	date = dfSelect['Start_Time']

	dataPerStation.append(len(dfSelect))
	numDayPerStation.append(len(pd.unique(date.apply(f))))

	print station, dataPerStation[len(dataPerStation)-1],\
				numDayPerStation[len(numDayPerStation)-1]

dataPerStation = np.array(dataPerStation)
numDayPerStation = np.array(numDayPerStation)



# generate clean data for good monitoring stations
goodStations = stationList[np.where(numDayPerStation > 300)[0]]

for stationChosen in goodStations:
	
	dfSelect = df[df['RCStation']==stationChosen]

	date = dfSelect['Start_Time']
	numDays = len(pd.unique(date.apply(f)))
	dfSelect=dfSelect.set_index(date)

	dfSelect = dfSelect.drop('RCStation',axis=1)

	allDirections = pd.unique(dfSelect['Direction'])
	dfSelect = dfSelect[dfSelect['Direction']==allDirections[0]]
	dfSelect = dfSelect.drop('Direction',axis=1)

	# aggregate all lanes, generate a time series object
	grouped = dfSelect['Count'].groupby(dfSelect['Start_Time'])
	ts = grouped.sum()

	# check interval
	segStart = ts.index[0]
	SegList = []
	segLength = []
	badData = False

	for i in range(len(ts)-1):
		delta = ts.index[i+1] - ts.index[i]
		intv = delta.total_seconds()
		
		if intv<3000 :
			badData = True
		if intv>3600 :#| delta.days>0:
			segEnd = ts.index[i]
			newSegLength = (segEnd - segStart).total_seconds()
			print segStart, segEnd, newSegLength
			SegList.append([segStart, segEnd])
			segLength.append(newSegLength)
			segStart = ts.index[i+1]

	longSeg = np.argmax(np.array(segLength))
	cleanData = ts[SegList[longSeg][0]:SegList[longSeg][1]]

	if badData==False:
		# write cleaned data to file
		fileName = 'data/cleanTrafficData' + str(stationChosen) +'.csv'
		outfile = open(fileName,'w')
		a = csv.writer(outfile)
		data = [['timestamp', 'hourly_traffic_count'],
		        ['datetime', 'float'],
		        ['T', '']]
		a.writerows(data)

		cleanData.to_csv(outfile)
		outfile.close()

plt.figure()
cleanData.plot()
plt.ylabel('Traffic Volumn (Hourly Count)')






# fileName = 'cleanTrafficData.csv'
# csvfile = open(fileName)
# csvreader = csv.reader(csvfile, delimiter=',')
# headline = csvreader.next()



# plot data for one station
stationChosen = stationList[0:2]
tsList = []
for station in stationChosen:
	dfSelect = df[df['RCStation']==station]
	dfSelect = dfSelect.drop('RCStation',axis=1)
	dfSelect=dfSelect.set_index(dfSelect['Start_Time'])

	allDirections = pd.unique(dfSelect['Direction'])
	dfSelect = dfSelect[dfSelect['Direction']==allDirections[0]]
	dfSelect = dfSelect.drop('Direction',axis=1)

	# aggregate all lanes, generate a time series object
	grouped = dfSelect['Count'].groupby(dfSelect['Start_Time'])
	ts = grouped.sum()
	tsList.append(ts)

# find date time index that are shared across the two series
dateTimeShared = set(tsList[0].index)
for i in range(1,len(tsList)):
	dateTimeShared = dateTimeShared.intersection(set(tsList[i].index))

# get date time sorted again
dateTimeShared = list(dateTimeShared)
dateTimeShared = pd.DataFrame(dateTimeShared).sort(columns = 0)
dateTimeShared.set_index(dateTimeShared[0])
dateTimeShared = Series(dateTimeShared)
# check interval
segStart = dateTimeShared[0]
SegList = []
segLength = []
for i in range(len(dateTimeShared)-1):
	delta = dateTimeShared[i+1] - dateTimeShared[i]
	intv = delta.total_seconds()
	
	if intv>3600 :#| delta.days>0:
		segEnd = dateTimeShared[i]
		newSegLength = (segEnd - segStart).total_seconds()
		print segStart, segEnd, newSegLength
		SegList.append([segStart, segEnd])
		segLength.append(newSegLength)
		segStart = dateTimeShared[i+1]

longSeg = np.argmax(np.array(segLength))
print " longest segment: ", SegList[longSeg]

ts = tsList[0]
nRows = len(ts[SegList[longSeg][0]:SegList[longSeg][1]])
combineCount = np.zeros((nRows,len(tsList)))
for i in range(len(tsList)):
	ts = tsList[i][SegList[longSeg][0]:SegList[longSeg][1]]
	combineCount[:,i] = ts

cleanData2 = pd.DataFrame(combineCount, index=ts.index, columns = stationChosen)

plt.figure()
cleanData2.plot()
plt.ylabel('Traffic Volumn (Hourly Count)')

# write cleaned data to file
fileName = 'cleanTrafficData2.csv'
outfile = open(fileName,'w')
a = csv.writer(outfile)
data = [['timestamp', 'hourly_traffic_count1', 'hourly_traffic_count2'],
        ['datetime', 'float', 'float'],
        ['T', '', '']]
a.writerows(data)
cleanData2.to_csv(outfile, header=False)
outfile.close()