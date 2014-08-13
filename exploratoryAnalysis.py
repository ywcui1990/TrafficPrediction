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
This script performed exploratory analysis with the data 

It generated a weekly pattern (in units of hours) and seasonal pattern
(in units of weeks) for each monitoring station

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


datapath = './data/'
datafiles = [ f for f in listdir(datapath) if isfile(join(datapath,f)) ]
datafiles = datafiles[1:]

# datafiles = ['cleanTrafficData30291_out.csv']


for i in range(len(datafiles)):
	if datafiles[i][-4:] == '.csv' and datafiles[i][:5]=='clean':		
		print i, datafiles[i]
	else:
		continue

	fileName = datafiles[i]

	df = pd.read_csv(datapath+fileName, skiprows=[1,2])

	df.columns = ['Start_Time','Count']
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
	plt.savefig('seasonalPattern/'+fileName.split('_')[0]+'.png')


	weekDayAvg = pd.groupby(df["Count"],df['WeekdayHour']).mean()	
	plt.close('all')
	plt.figure()
	ax = plt.subplot(111)
	ax.plot(weekDayAvg)
	ax.set_ylabel('Hourly Count')

	ind = np.arange(7)*24+12
	ax.set_xticks(ind)
	ax.set_xticklabels( ('Mon','Tue','Wed','Thu','Fri','Sat','Sun') )
	plt.savefig('dayWeekPattern/'+fileName.split('_')[0]+'.png')

