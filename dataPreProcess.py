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


import pandas as pd 
import numpy as np
from pandas import DataFrame, Series
import csv

import matplotlib.pyplot as plt

from pylab import *
if isinteractive() is not True:
  ion()

def readInData(fileName):
	print " Read in data, this several minutes, sit back and relax"
	# parse date while reading the data (takes a while)
	dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M')
	df = pd.read_csv(fileName, parse_dates=['Start_Time'], \
			date_parser=dateparse)

	return df

def getDayOfYear(date):
	# extract day of the year 
	dayOfYear = date.dayofyear
	return dayOfYear

def getNumDataPerStation(df):
	stationList = pd.unique(df['RCStation'])

	# calculate number of days and data points per monitoring station
	dataPerStation = []
	numDayPerStation = []

	for station in stationList:
		
		dfSelect = df[df['RCStation']==station]
		date = dfSelect['Start_Time']

		dataPerStation.append(len(dfSelect))
		numDayPerStation.append(len(pd.unique(date.apply(getDayOfYear))))

		print station, dataPerStation[len(dataPerStation)-1],\
					numDayPerStation[len(numDayPerStation)-1]

	dataPerStation = np.array(dataPerStation)
	numDayPerStation = np.array(numDayPerStation)
	return (dataPerStation, numDayPerStation)

def saveCleanData(cleanData, stationChosen):
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
	print "Saved ", fileName

def selectGoodStations(df, numDayPerStation, minDays=60):
	# only consider stations with more than [minDays] days data
	# save clean data for each good monitoring stations in ./data/

	goodStations = stationList[np.where(numDayPerStation > minDays)[0]]

	for stationChosen in goodStations:
		
		dfSelect = df[df['RCStation']==stationChosen]		
		date = dfSelect['Start_Time']
		
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

		notHourlyCount = False

		for i in range(len(ts)-1):
			delta = ts.index[i+1] - ts.index[i]
			intv = delta.total_seconds()
			
			if intv<3600 :
				notHourlyCount = True
			if intv>3600 :
				segEnd = ts.index[i]
				newSegLength = (segEnd - segStart).total_seconds()
				
				SegList.append([segStart, segEnd])
				segLength.append(newSegLength)
				segStart = ts.index[i+1]

		longSeg = np.argmax(np.array(segLength))
		longSegLength = max(segLength)/(60*60*24) # days

		if notHourlyCount==False and longSegLength>minDays:
			cleanData = ts[SegList[longSeg][0]:SegList[longSeg][1]]
			saveCleanData(cleanData, stationChosen)

if __name__ == "__main__":

	# path to the data file
	fileName = 'data/VOL_2011.csv'

	df = readInData(fileName)
	# stationList = pd.unique(df['RCStation'])

	(dataPerStation, numDayPerStation) = getNumDataPerStation(df)

	# select stations with 
	selectGoodStations(df, numDayPerStation)

	# plt.figure()
	# cleanData.plot()
	# plt.ylabel('Traffic Volumn (Hourly Count)')



	# fileName = 'cleanTrafficData.csv'
	# csvfile = open(fileName)
	# csvreader = csv.reader(csvfile, delimiter=',')
	# headline = csvreader.next()



	# # plot data for one station
	# stationChosen = stationList[0:2]
	# tsList = []
	# for station in stationChosen:
	# 	dfSelect = df[df['RCStation']==station]
	# 	dfSelect = dfSelect.drop('RCStation',axis=1)
	# 	dfSelect=dfSelect.set_index(dfSelect['Start_Time'])

	# 	allDirections = pd.unique(dfSelect['Direction'])
	# 	dfSelect = dfSelect[dfSelect['Direction']==allDirections[0]]
	# 	dfSelect = dfSelect.drop('Direction',axis=1)

	# 	# aggregate all lanes, generate a time series object
	# 	grouped = dfSelect['Count'].groupby(dfSelect['Start_Time'])
	# 	ts = grouped.sum()
	# 	tsList.append(ts)

	# # find date time index that are shared across the two series
	# dateTimeShared = set(tsList[0].index)
	# for i in range(1,len(tsList)):
	# 	dateTimeShared = dateTimeShared.intersection(set(tsList[i].index))

	# # get date time sorted again
	# dateTimeShared = list(dateTimeShared)
	# dateTimeShared = pd.DataFrame(dateTimeShared).sort(columns = 0)
	# dateTimeShared.set_index(dateTimeShared[0])
	# dateTimeShared = Series(dateTimeShared)
	# # check interval
	# segStart = dateTimeShared[0]
	# SegList = []
	# segLength = []
	# for i in range(len(dateTimeShared)-1):
	# 	delta = dateTimeShared[i+1] - dateTimeShared[i]
	# 	intv = delta.total_seconds()
		
	# 	if intv>3600 :#| delta.days>0:
	# 		segEnd = dateTimeShared[i]
	# 		newSegLength = (segEnd - segStart).total_seconds()
	# 		print segStart, segEnd, newSegLength
	# 		SegList.append([segStart, segEnd])
	# 		segLength.append(newSegLength)
	# 		segStart = dateTimeShared[i+1]

	# longSeg = np.argmax(np.array(segLength))
	# print " longest segment: ", SegList[longSeg]

	# ts = tsList[0]
	# nRows = len(ts[SegList[longSeg][0]:SegList[longSeg][1]])
	# combineCount = np.zeros((nRows,len(tsList)))
	# for i in range(len(tsList)):
	# 	ts = tsList[i][SegList[longSeg][0]:SegList[longSeg][1]]
	# 	combineCount[:,i] = ts

	# cleanData2 = pd.DataFrame(combineCount, index=ts.index, columns = stationChosen)

	# plt.figure()
	# cleanData2.plot()
	# plt.ylabel('Traffic Volumn (Hourly Count)')

	# # write cleaned data to file
	# fileName = 'cleanTrafficData2.csv'
	# outfile = open(fileName,'w')
	# a = csv.writer(outfile)
	# data = [['timestamp', 'hourly_traffic_count1', 'hourly_traffic_count2'],
	#         ['datetime', 'float', 'float'],
	#         ['T', '', '']]
	# a.writerows(data)
	# cleanData2.to_csv(outfile, header=False)
	# outfile.close()