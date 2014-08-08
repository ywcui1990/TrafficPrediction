from os import listdir
from os.path import isfile, join
import swarm

datapath = './data/'
datafiles = [ f for f in listdir(datapath) if isfile(join(datapath,f)) ]
datafiles = datafiles[1:]

for i in range(14,len(datafiles)):
	swarm.swarm(datapath + datafiles[i])