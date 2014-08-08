import pandas as pd 
import numpy as np
from pandas import DataFrame, Series
import csv

import matplotlib.pyplot as plt

from pylab import *
if isinteractive() is not True:
  ion()


def calculateErrorRate(measured, predicted):
	measured = np.array(measured)
	predictDayAvg = np.array(predicted)	
	errorRate = mean(abs(measured-predictDayAvg)/measured)
	return errorRate


from os import listdir
from os.path import isfile, join

import run

datapath = './'
datafiles = [ f for f in listdir(datapath) if isfile(join(datapath,f)) ]
datafiles = datafiles[1:]

for i in range(len(datafiles)):
	if datafiles[i][-8:] == '_out.csv' and datafiles[i][:5]=='clean':		
		print datafiles[i]

fileName = "cleanTrafficData10012_out.csv"
csvfile = open(fileName)
csvreader = csv.reader(csvfile, delimiter=',')
headline = csvreader.next()
csvfile.close()

df = pd.read_csv(fileName)
df.columns = ['Start_Time','Count','Prediction']
df['Start_Time'] = pd.to_datetime(df['Start_Time'])
f = lambda x: x.hour
df['Hours'] = df['Start_Time'].apply(f)
g = lambda x: x.dayofweek
df['Weekday'] = df['Start_Time'].apply(g)

df['WeekdayHour'] = df['Weekday']*24 + df['Hours']

nTrain = len(df)/2
dfTrain = df[1:nTrain]
dfTest = df[nTrain:]
predictionDayAvg = pd.groupby(dfTrain["Count"],dfTrain['Hours']).mean()
predictionWeekDayAvg = pd.groupby(dfTrain["Count"],dfTrain['WeekdayHour']).mean()

measured = []
predictDayAvg = []
predictDayWeekAvg = []
predictionCLA = []
predictedShifer = []
for i in range(nTrain+1, len(df)-1):
	measured.append(dfTest['Count'][i])
	predictDayAvg.append(predictionDayAvg[dfTest['Hours'][i]]) 
	predictDayWeekAvg.append(predictionWeekDayAvg[dfTest['WeekdayHour'][i]])
	predictionCLA.append(dfTest['Prediction'][i-1])
	predictedShifer.append(dfTest['Count'][i-1])


measured = np.array(measured)
predictDayAvg = np.array(predictDayAvg)
predictDayWeekAvg = np.array(predictDayWeekAvg)
predictionCLA = np.array(predictionCLA)	
predictedShifer = np.array(predictedShifer)	

prediction = pd.DataFrame(np.array((measured, predictDayAvg, predictDayWeekAvg, predictionCLA, predictedShifer)).T,
	columns=['Measure','Day Avg', 'Day Week Avg','CLA', 'Shifter'])

ErrorRates = [calculateErrorRate(measured, predictedShifer),
							calculateErrorRate(measured, predictDayAvg),														
							calculateErrorRate(measured, predictDayWeekAvg),							
							calculateErrorRate(measured, predictionCLA)]

print "Naive Shifter: ", ErrorRates[0]
print "Day Avg", ErrorRates[1]
print "Week-Day Avg", ErrorRates[2]
print "CLA: ",ErrorRates[3]

plt.close('all')
plt.figure()
width  =.35
ax = plt.subplot(111)
ind = np.arange(len(ErrorRates))
ax.bar(ind, ErrorRates, color='k')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Naive Shifter', 'Day Avg','Day-Week Avg', 'CLA') )