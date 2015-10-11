# -*- coding: utf-8 -*-

# version 0.1, 20151011, hvdwolf@gmnail.com
# extremely quick and dirty approach. Needs clean up, improvements, modularisation
# Currently uses OS curl to post. Needs to be python posting via urllibor pycurl


import urllib, urllib2, os
#from xml.etree import ElementTree as ET

### Pimatic settings ###
# localhost is fine when running from your pimatic server. Otherwise change to suitable ip address or dns. Can be https as well.
pimatic_server = 'localhost'
# user and password. I prefer a special posting user having a role of varposter with only  "variables": "write" in the varposter role. Rest to "none" or false.
pimatic_user = 'username'
pimatic_pass = 'password'

### Weer actueel ###
# Has much better spreading. Check update sequence from relevant page
# http://www.hetweeractueel.nl/
# Is not really free
WeerActueel = "NO" # use in script: YES or NO
WALocation = "Zwolle"
WAURL = 'http://www.hetweeractueel.nl/weer/' + WALocation + '/actueel/'


### KNMI ###
# central public FTP page ftp://ftp.knmi.nl/pub_weerberichten/tabel_10min_data.html
# updated every 10 minutes
KNMI = "YES"  # use in script: YES or NO
KNMILocation = "Heino"
KNMIURL = 'ftp://ftp.knmi.nl/pub_weerberichten/tabel_10min_data.html'
# Define an identifying column list. Add some empty entries due to possible trailing rubbish
knmi_columns = ['Locatie', 'Weer', 'Temperatuur', 'RV', 'Wind richting', 'Wind (m/s)', 'Zicht (m)', 'Druk (hPa)', '', '', '' ]

##########################################################################
#### It should not be necessary to change anything below these lines #####
##########################################################################

# Initialize some internal variables
pim_user_pass = pimatic_user + ':' + pimatic_pass
curl_prefix = 'curl --insecure -X PATCH --header "Content-Type:application/json" --data \'{"type": "value", "valueOrExpression": "'
pim_server_url = pimatic_server + '/api/variables/'


# Start the real work

if WeerActueel == "YES":
        response = urllib2.urlopen(WAURL)
        html = response.read()
        split_string = 'Actueel weer ' + WALocation
        tmppage = html.split(split_string)
        subpage = str(tmppage[2])
        #print(subpage)
        tmppage = subpage.split('<table>')
        subpage = '<table>' + str(tmppage[1])
        tmppage = subpage.split('</table>')
        tabel = str(tmppage[0]) + '</table>'
        print(tabel)

if KNMI == 'YES':
        response = urllib2.urlopen(KNMIURL)
        html = response.read()
        tmppage = html.split(KNMILocation + '</td>')
        subpage = str(tmppage[1])
        tmppage = subpage.split('</tr>')
        table = str(tmppage[0])
        table = table.replace('&nbsp;</td>', '', 99).replace('<td align=right>', '', 99).replace('  ', '', 999).replace('<td>', '', 999).replace('</td>', '', 99)
        counter = 0
        for line in table.splitlines():
                # Finally remove still redundant spaces
                line = line.replace(' ', '', 99)
                # Add units to variableDevice in pimatic
                if knmi_columns[counter] == 'Locatie':
                        os.system(curl_prefix + KNMILocation + '"}\'  --user "' + pim_user_pass + '" ' + pim_server_url +'knmi-locatie')
                if knmi_columns[counter] == 'Temperatuur':
                        os.system(curl_prefix + line + '"}\'  --user "' + pim_user_pass + '" ' + pim_server_url +'knmi-temperatuur')
                if knmi_columns[counter] == 'RV':
                        os.system(curl_prefix + line + '"}\'  --user "' + pim_user_pass + '" ' + pim_server_url +'knmi-rv')
                if knmi_columns[counter] == 'Wind richting':
                        os.system(curl_prefix + line + '"}\'  --user "' + pim_user_pass + '" ' + pim_server_url +'knmi-wr')
                if knmi_columns[counter] == 'Wind (m/s)':
                        os.system(curl_prefix + line + '"}\'  --user "' + pim_user_pass + '" ' + pim_server_url +'knmi-ws')
                if knmi_columns[counter] == 'Zicht (m)':
                        os.system(curl_prefix + line + '"}\'  --user "' + pim_user_pass + '" ' + pim_server_url +'knmi-zicht')
                if knmi_columns[counter] == 'Druk (hPa)':
                        os.system(curl_prefix + line + '"}\'  --user "' + pim_user_pass + '" ' + pim_server_url +'knmi-druk')
                counter += 1