import pandas as pd 
import numpy as np
from pandas import DataFrame, Series
import csv

import matplotlib.pyplot as plt

from pylab import *
if isinteractive() is not True:
  ion()

from os import listdir
from os.path import isfile, join


def calculateErrorRate(measured, predicted):
	measured = np.array(measured)
	predicted = np.array(predicted)	
	errorRate = mean(abs(measured-predicted)/mean(measured))
	# errorRate = mean(abs(measured-predicted)/mean(measured))
	return errorRate


datapath = './'
datafiles = [ f for f in listdir(datapath) if isfile(join(datapath,f)) ]
datafiles = datafiles[1:]

ErrorRatesAll = []

for i in range(len(datafiles)):
	if datafiles[i][-8:] == '_out.csv' and datafiles[i][:5]=='clean':		
		print i, datafiles[i]
	else:
		continue

	fileName = datafiles[i]
	# fileName = "cleanTrafficData10012_out.csv"
	# fileName = "cleanTrafficData330378_out.csv"
	csvfile = open(fileName)
	csvreader = csv.reader(csvfile, delimiter=',')
	headline = csvreader.next()
	csvfile.close()

	df = pd.read_csv(fileName)
	if len(df)<500:
		continue

	df.columns = ['Start_Time','Count','Prediction']
	df['Start_Time'] = pd.to_datetime(df['Start_Time'])
	f = lambda x: x.hour
	df['Hours'] = df['Start_Time'].apply(f)
	g = lambda x: x.dayofweek
	df['Weekday'] = df['Start_Time'].apply(g)
	k = lambda x: x.weekofyear
	df['WeekofYear'] = df['Start_Time'].apply(k)
	df['WeekdayHour'] = df['Weekday']*24 + df['Hours']
	avgWeek = pd.groupby(df["Count"],df['WeekofYear']).sum()
	avgWeek = avgWeek[1:len(avgWeek)-1]
	plt.close('all')
	plt.plot(avgWeek.index, avgWeek)
	plt.xlabel(' Week of Year')
	plt.ylabel(' Weekly Traffic Count ')
	plt.savefig('seasonalPattern/'+fileName.split('_')[0]+'.pdf')

	nTrain = int(len(df)*.5)
	dfTrain = df[1:nTrain]
	dfTest = df[nTrain:]

	# dfTrain = df[1:len(df)]
	# dfTest = df[1:len(df)]	
	predictionDayAvg = pd.groupby(dfTrain["Count"],dfTrain['Hours']).mean()

	predictionWeekDayAvg = pd.groupby(dfTrain["Count"],dfTrain['WeekdayHour']).mean()

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

	# plt.close('all')
	# plt.figure()
	# ax = plt.subplot(111)
	# ax.plot(predictionWeekDayAvg)
	# ax.set_ylabel('Hourly Count')

	# ind = np.arange(7)*24+12
	# ax.set_xticks(ind)
	# ax.set_xticklabels( ('Mon','Tue','Wed','Thu','Fri','Sat','Sun') )

	# # plt.title('Error Rate '+str(ErrorRates[2])+' '+str(str(ErrorRates[3])))
	# plt.savefig('dayWeekPattern/'+fileName.split('_')[0]+'.pdf')

	ErrorRatesAll.append(ErrorRates)

	print "Naive Shifter: ", ErrorRates[0]
	print "Day Avg", ErrorRates[1]
	print "Week-Day Avg", ErrorRates[2]
	print "CLA: ",ErrorRates[3]


ErrorRatesAll = np.array(ErrorRatesAll)*100
N = ErrorRatesAll.shape[0]

MeanErrorRate = np.mean(ErrorRatesAll, axis=0)
print MeanErrorRate
errorSEM = np.std(ErrorRatesAll,axis=0)/sqrt(N)
plt.close('all')
plt.figure()
ax = plt.subplot(111)
# plt.boxplot(ErrorRatesAll)
ind = np.arange(4)
ax.bar(ind, MeanErrorRate, color='k', yerr=errorSEM)
width  =.35
ind = np.arange(4)
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Naive Shifter', 'Day Avg','Day-Week Avg', 'CLA') )
ax.set_ylabel("Error Rate (%)")
plt.savefig('result/ErrorRate.pdf')
# 
# ind = np.arange(len(ErrorRates))
# ax.bar(ind, ErrorRates, color='k')
