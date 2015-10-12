# pimatic-knmi
Simple python 2 script to retrieve data from KNMI and use it in pimatic

You need to change some settings in the top of your script for your pimatic server
<pre>
### Pimatic settings ###
# localhost is fine when running from your pimatic server. Otherwise change to suitable ip address or dns. Can be https as well.
pimatic_server = 'localhost'
# user and password. I prefer a special posting user having a role of varposter with only  "variables": "write" in the varposter role. Rest to "none" or false.
pimatic_user = 'username'
pimatic_pass = 'password'
</pre>

Next to that you need to specify your location. Note that KNMI has not weather stations everywhere so first check the page at ftp://ftp.knmi.nl/pub_weerberichten/tabel_10min_data.html before you add a KNMI location. 
<pre>
### KNMI ###
# central public FTP page ftp://ftp.knmi.nl/pub_weerberichten/tabel_10min_data.html
# updated every 10 minutes
KNMI = "YES"  # use in script: YES or NO
KNMILocation = "Heino"
</pre>

And finally schedule it in your cron (or as a rule or device in pimatic).
In cron (every 10 minute):
<pre>*/10 * * * * <some_path_to_your>/weeroverzicht.py > /dev/null 2>&1</pre>
