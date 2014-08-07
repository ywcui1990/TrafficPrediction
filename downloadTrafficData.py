# This script will download traffic data from Department of Transportation
# of the New York State

# https://www.dot.ny.gov/divisions/engineering/technical-services/highway-data-services/hdsb

import urllib2

if __name__ == "__main__":
	
	url = "https://www.dot.ny.gov/divisions/engineering/technical-services/highway-data-services/hdsb/repository/VOL_2011.zip"
	# url = "https://www.dot.ny.gov/divisions/engineering/technical-services/highway-data-services/hdsb/repository/New_York_VOL_2011.csv"
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

# if __name__ == "__main__":
# 	downloadData()