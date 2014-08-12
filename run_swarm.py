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

from os import listdir
from os.path import isfile, join
import re
import swarm

datapath = './data/'
datafiles = [ f for f in listdir(datapath) 
		if isfile(join(datapath,f)) and  re.search('^cleanTrafficData', f)]

print " Run Swarming Over ", len(datafiles), "data files"
print " This could take a long time"

for i in range(len(datafiles)):
	swarm.swarm(datapath + datafiles[i])