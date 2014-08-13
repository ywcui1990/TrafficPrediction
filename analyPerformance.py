#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

'''
This script calculated the quality of prediction using a simple error metric

The performance of CLA is compared with three other simple methods:
(1) Naive shifter: predict t+1 based on data of to_datetime
(2) Historical Average (Day time): predict based on historical average of
																		that time of the day
(3) Historical Average (Week-day time): predict based on historical average 
														using both weekday and time of the day

'''
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


datapath = './prediction/'
datafiles = [ f for f in listdir(datapath) if isfile(join(datapath,f)) ]
datafiles = datafiles[1:]


ErrorRatesAll = []

for i in range(len(datafiles)):
	if datafiles[i][-8:] == '_out.csv' and datafiles[i][:5]=='clean':		
		print i, datafiles[i]
	else:
		continue

	fileName = datapath+datafiles[i]

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
	k = lambda x: x.weekofyear
	df['WeekofYear'] = df['Start_Time'].apply(k)
	df['WeekdayHour'] = df['Weekday']*24 + df['Hours']

	nTrain = int(len(df)*.5)
	dfTrain = df[1:nTrain]
	dfTest = df[nTrain:]

	# use historical average as predictor
	predictionDayAvg = pd.groupby(dfTrain["Count"],dfTrain['Hours']).mean()
	predictionWeekDayAvg = pd.groupby(dfTrain["Count"],dfTrain['WeekdayHour']).mean()

	# generate prediction with different methdos	
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

	# calculate error rate with different method
	ErrorRates = [calculateErrorRate(measured, predictedShifer),
								calculateErrorRate(measured, predictDayAvg),														
								calculateErrorRate(measured, predictDayWeekAvg),							
								calculateErrorRate(measured, predictionCLA)]


	ErrorRatesAll.append(ErrorRates)

	print "Naive Shifter: ", ErrorRates[0]
	print "Day Avg", ErrorRates[1]
	print "Week-Day Avg", ErrorRates[2]
	print "CLA: ",ErrorRates[3]


ErrorRatesAll = np.array(ErrorRatesAll)*100
N = ErrorRatesAll.shape[0]

MeanErrorRate = np.mean(ErrorRatesAll, axis=0)
print MeanErrorRate

# plot error for different prediction methods
errorSEM = np.std(ErrorRatesAll,axis=0)/sqrt(N)
plt.close('all')
plt.figure()
ax = plt.subplot(111)

ind = np.arange(4)
ax.bar(ind, MeanErrorRate, color='k', yerr=errorSEM)
width  =.35
ind = np.arange(4)
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Naive Shifter', 'Day Avg','Day-Week Avg', 'CLA') )
ax.set_ylabel("Deviation from measured (%)")
plt.savefig('result/ErrorRate.pdf')
# 

