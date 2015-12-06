#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Version 20151206
# make python3 and python 2 compatible

# Version 0.2, 20151206, Full rewrite of script. Also add new Chill variable
# version 0.1, 20151011, hvdwolf@gmnail.com
# extremely quick and dirty approach. Needs clean up, improvements, modularisation
# Currently uses OS curl to post. Needs to be python posting via urllib or pycurl

# ToDo: Try to add weeractueel and full table download from KNMI and xml parse it. Requires currently
# more effort due to non-DTD characters.

import urllib, os
from xml.etree import ElementTree as ET
#from html_table_parser import HTMLTableParser

try:
	# For python3
	from urllib.request import urlopen
	python3 = "YES"
except ImportError:
	# Use python2
	from urllib2 import urlopen
	python3 = "NO"

### Pimatic settings ###
# localhost is fine when running from your pimatic server. Otherwise change to suitable ip address or dns. 
# Can be https as well. Also: if you use another port then 80 or 443 do not forget to add the port number.
pimatic_server = 'localhost'
# user and password. I prefer a special posting user having a role of varposter with only  "variables": "write" in the varposter role. Rest to "none" or false.
pimatic_user ='username'
pimatic_pass = 'password'

### KNMI ###
# central public FTP page ftp://ftp.knmi.nl/pub_weerberichten/tabel_10min_data.html
# updated every 10 minutes
KNMI = "YES"  # use in script: YES or NO
KNMILocation = "Heino"

# DEBUG True or False. If True some extra prints to screen will be done
DEBUG = False
##########################################################################
#### It should not be necessary to change anything below these lines #####
##########################################################################

# Initialize some internal variables
pim_user_pass = pimatic_user + ':' + pimatic_pass
curl_prefix = 'curl --silent --insecure -X PATCH --header "Content-Type:application/json" --data \'{"type": "value", "valueOrExpression": "'
pim_server_url = pimatic_server + '/api/variables/'
KNMIURL = 'ftp://ftp.knmi.nl/pub_weerberichten/tabel_10min_data.html'

# Start the real work
if KNMI == 'YES':
	response = urlopen(KNMIURL)
	html = response.read()
	if python3 == "YES":
		html = str( html, encoding='utf8' )
	html = html.replace('<br>(&deg;C)', '', 99).replace('&nbsp;', '', 9999).replace('<br>(%)', '', 99).replace('<br>(m/s)', 'ms', 99)
	html = html.replace('<br>(m)', '', 99).replace('<br>(hPa)', '', 99).replace('class="trcolor"', '',999).replace(' align=right', '', 999)
	#print(html)
	tmppage = html.split('<table width') # 2 instances
	subpage = str(tmppage[2])
	tmppage = subpage.split('</table>')
	table = '<table width' + str(tmppage[0]) + '</table>'
	#print(table)
	xmltable = ET.XML(table)
	rows = iter(xmltable)
	headers = [col.text.replace(' ', '',99) for col in next(rows)]
	if DEBUG:
		print(headers)
	for row in rows:
		# check if not text/value (None), else replace all redundant hundreds of spaces and then add the ones back in halfbewolkt, zwaarbewolkt and geheelbewolkt.
		values = ['' if col.text is None else col.text.replace(' ', '',99).replace('bewolkt', ' bewolkt',99) for col in row]
		#print(values)
		if KNMILocation in values:
			counter = 0
			for value in values:
				if DEBUG:
					print('header: ' + str(headers[counter]) + ', value: ' + str(value))
				# The headers are 'Station', 'Weer', 'Temp', 'Chill', 'RV', 'Wind', 'Windms', 'Zicht', 'Druk'
				# The headers are the variables send to pimatic
				os.system(curl_prefix + str(value) + '"}\'  --user "' + pim_user_pass + '" ' + pim_server_url + str(headers[counter]))
				counter += 1 
		#if DEBUG:
		#	print(dict(zip(headers, values)))
		#	print('\n\n')
