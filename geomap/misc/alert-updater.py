#!/usr/bin/python
import os
import subprocess
import StringIO
import re
import sys
import pymssql
sys.path.append('/var/django/web/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'web.settings')

#from django.core.management import setup_environ

#setup_environ(settings)
from maps.models import Coordinates, Alert
import getgeo



class Something:
    pass



startline = re.compile("^\s\w")
blankline = re.compile("^\s?\n$")
dataline = re.compile("^\t")
proc = subprocess.Popen("/opt/scripts/pingfails.sh", stdout=subprocess.PIPE)
text, err = proc.communicate()
stringreader = StringIO.StringIO(text)
alerts = []

alert = ''
n = 0
while True:
    line = stringreader.readline()
    if not line:
        break

    if re.match(startline, line):
        if n > 0:
            temp = Something()
            temp.node = nodename
            temp.data = alert
            alerts.append(temp)

            nodename = line.strip().replace('\x00','')
            alert = ''
            n += 1
    
        else:
            nodename = line.strip().replace('\x00','')
            alert = ''
            n += 1        
        continue

    elif re.match(dataline, line):
        fline = line.replace('\x00','')
        alert += fline
        continue
    elif re.match(blankline, line):
        continue
        
    else:
        continue
            
alerts.pop(0)
alerts.pop(0)
Alert.objects.all().delete()
conn = pymssql.connect(dbserver, user, password, db)
cursor = conn.cursor(as_dict=True)



for a in alerts:
    
    dnsname = a.node
    dnsname = dnsname.rstrip()
    working = a.data.split('\n')
    location = working.pop(0).strip()
    alert = ''.join(working).strip().replace('\t','').strip()
    
    

    location = location.replace('&','')

    
    if dnsname == None:
        continue

    if location is None:
        print(a.node + 'no location')
        continue 
    cursor.execute("Select Status from Asset_Table where DNSname = '%s'" % dnsname)
    try:
        row = cursor.fetchone()
        status = row["Status"]
    except Exception, e:
        continue
    if status != 'Production':
        continue
    qtest = Coordinates.objects.filter(location=location)
    if len(qtest) == 0:
        loc = location
        lat, lng = getgeo.geoCode(location)
        new_entry = Coordinates(location=loc, lat=lat, lng=lng)
        new_entry.save()

    qtest2 = Alert.objects.filter(node=a.node).filter(location=location).filter(text=alert)
    if len(qtest2) == 0:
        new_entry = Alert(node=a.node, location=location, text=alert)
        new_entry.save()



conn.close()





 
            
    


