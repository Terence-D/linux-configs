import requests
import json
import pytz
from datetime import datetime,timezone,timedelta

### set these variables
### set these variables
### set these variables
serverUrl = 'http://localhost:8096/devices'
apiToken = 'YOUR-API-TOKEN'
minutesToCheck = 10
logFile = '/path/jellyfin-status.txt'
### recommend to not change anything below
### recommend to not change anything below
### recommend to not change anything below

def saveOutput(output, mode):
    with open(logFile, mode) as f:
        print(output, file=f)

#load in our request
request = requests.get(serverUrl, headers = {"X-MediaBrowser-Token": apiToken})
jsonResult = json.loads(request.text)

#get the datetime from 'minutesToCheck' Minutes ago
now = datetime.now(timezone.utc)
timecheck = now - timedelta(minutes=minutesToCheck)
logFileDate = now.astimezone().strftime("%d/%m/%Y %H:%M:%S")

#default us to finding nothing
activeDevices = False
output = ''

for i in jsonResult['Items']:
    lastActivity = datetime.strptime(i['DateLastActivity'][:19], '%Y-%m-%dT%H:%M:%S')
    lastActivityZ = pytz.utc.localize(lastActivity)
    if (lastActivityZ > timecheck):
        #someones watching, don't power down
        activeDevices = True
        output += str.format('{0}   {1} was active within the last {2} minute(s)\n', logFileDate, i['Name'], minutesToCheck)

if (activeDevices):
    saveOutput(output, 'w')
    exit(1)
else:
    output = str.format('{0}   No devices found online', logFileDate)
    saveOutput(output, 'a')
    exit(0)