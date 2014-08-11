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
This script will download traffic data from Department of Transportation
of the New York State
After running the script, the data will be located in './data/VOL_2011.zip'

You may also download the data manually from this page
https://www.dot.ny.gov/divisions/engineering/technical-services/highway-data-services/hdsb
'''

import urllib2
import zipfile

if __name__ == "__main__":
	
	url = "https://www.dot.ny.gov/divisions/engineering/technical-services/highway-data-services/hdsb/repository/VOL_2011.zip"

	# open url
	u = urllib2.urlopen(url)

	# store data locally at this directory
	file_name = 'data/' + url.split('/')[-1]	
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)

	# read data in blocks
	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,

	f.close()

	# extract zip file
	with zipfile.ZipFile('./data/VOL_2011.zip', 'r') as zfile:
	    zfile.extractall('./data')
