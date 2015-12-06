# pimatic-knmi
Simple python (2 & 3 compatible) script to retrieve data from KNMI and use it in pimatic

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

And in pimatic you define in the <strong>"devices": [  .....  ]</strong> section something like:
<pre>    {
      "id": "KNMImeting",
      "//": "This variables Device is used to display the variables that will be updated by the external python script",
      "name": "KNMI meting",
      "class": "VariablesDevice",
      "variables": [
        {
          "name": "knmi-locatie",
          "expression": "$Station",
          "type": "string",
          "label": "Plaats",
          "discrete": true,
          "acronym": "Locatie"
        },
        {
          "name": "knmi-weer",
          "expression": "$Weer",
          "type": "string",
          "discrete": false
        },
        {
          "name": "knmi-temperatuur",
          "expression": "$Temp",
          "type": "number",
          "unit": "°C",
          "label": "Temperatuur",
          "discrete": false,
          "acronym": "T"
        },
        {
          "name": "knmi-chill",
          "expression": "$Chill",
          "type": "number",
          "unit": "°C",
          "label": "Chill Temperatuur",
          "discrete": false,
          "acronym": "T"
        },
        {
          "name": "knmi-luchtvochtigheid",
          "expression": "$RV",
          "type": "number",
          "unit": "%",
          "label": "RV",
          "discrete": false,
          "acronym": "RV"
        },
        {
          "name": "knmi-wr",
          "expression": "$Wind",
          "type": "string",
          "discrete": false,
          "acronym": "Wind"
        },
        {
          "name": "knmi-ws",
          "expression": "$Windms",
          "type": "number",
          "unit": "m/s",
          "label": "wind",
          "discrete": false,
          "acronym": "Wind (m/s)"
        },
        {
          "name": "knmi-zicht",
          "expression": "$Zicht",
          "type": "number",
          "unit": "m",
          "label": "zicht",
          "discrete": false,
          "acronym": "Zicht (m)"
        },
        {
          "name": "knmi-druk",
          "expression": "$Druk",
          "type": "number",
          "unit": "hPa",
          "label": "Druk",
          "discrete": false,
          "acronym": "Druk (hPa)"
        }
      ],
      "xAttributeOptions": [
        {
          "name": "knmi-locatie",
          "displaySparkline": false,
          "hidden": false
        },
        {
          "name": "knmi-weer",
          "displaySparkline": false,
          "hidden": true
        },
        {
          "name": "knmi-temperatuur",
          "displaySparkline": true,
          "hidden": false
        },
        {
          "name": "knmi-chill",
          "displaySparkline": true,
          "hidden": false
        },
        {
          "name": "knmi-luchtvochtigheid",
          "displaySparkline": true,
          "hidden": false
        },
        {
          "name": "knmi-wr",
          "displaySparkline": false,
          "hidden": false
        },
        {
          "name": "knmi-ws",
          "displaySparkline": false,
          "hidden": false
        },
        {
          "name": "knmi-zicht",
          "displaySparkline": false,
          "hidden": true
        },
        {
          "name": "knmi-druk",
          "displaySparkline": false,
          "hidden": true
        }
      ]
    },
</pre>


And in the <strong>"variables": [ ....  ]</strong>  section you need to define:</br>
(Of course you can leave the values empty as they will be automatically filled upon first push to pimatic)
<pre>
    {
      "name": "Station",
      "value": "Heino"
    },
    {
      "name": "Weer",
      "value": ""
    },
    {
      "name": "Temp",
      "value": 12
    },
    {
      "name": "Chill",
      "value": ""
    },
    {
      "name": "RV",
      "value": 75
    },
    {
      "name": "Wind",
      "value": "ZW"
    },
    {
      "name": "Windms",
      "value": 6
    },
    {
      "name": "Zicht",
      "value": ""
    },
    {
      "name": "Druk",
      "value": ""
    },
</pre>
