from os import listdir
from os.path import isfile, join

import run

datapath = './model_params/'
datafiles = [ f for f in listdir(datapath) if isfile(join(datapath,f)) ]
datafiles = datafiles[1:]

for i in range(len(datafiles)):
	if datafiles[i][-3:] == '.py' and datafiles[i][:5]=='clean':
		
		dataName = datafiles[i].split('_')[0]
		print datafiles[i], ' dataName ', dataName
		run.runModel(dataName, plot=False)