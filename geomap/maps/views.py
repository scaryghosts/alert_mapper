from django.shortcuts import render
from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
import random
# Create your views here.

from models import Coordinates, Alert, Cores, ActiveAlerts

def mapdex(request):
    
    class Holder:
        pass
   
    all_alerts = Alert.objects.all()
    
    nodelist = []
    for a in all_alerts:
        
        lat = ''
        lng = ''
        loc = a.location
        qt1 = Coordinates.objects.filter(location=loc)
        if qt1:
            locitem = Coordinates.objects.get(location=loc)
            lat = locitem.lat
            lng = locitem.lng
        else:
            continue
        tempholder = Holder()
        tempholder.Node = a.node
        tempholder.Lat = lat
        tempholder.Lng = lng
        tempholder.Location = loc
        tempholder.Text = a.text
        tempholder.Center = lat + ',' + lng

        nodelist.append(tempholder)

    return render_to_response('mapdex.html', {'items': nodelist})

def mapshow(request):

    class Holder:
        pass

    all_cores = Cores.objects.all()
    all_alerts = Alert.objects.all()
    nodelistdict = {}
    nodelist = []
    for a in all_cores:

        lat = ''
        lng = ''
        loc = a.location
        
        qt1 = Coordinates.objects.filter(location=loc)
        if qt1:
            locitem = Coordinates.objects.get(location=loc)
            lat = locitem.lat
            lng = locitem.lng
            lat = str(float(lat) - .00008)
        else:
            continue
        tempholder = Holder()
        tempholder.Node = a.dnsname
        tempholder.Lat = lat
        tempholder.Lng = lng
        tempholder.Location = loc
        tempholder.Center = lat + ',' + lng
        tempholder.Icon = "../static/player-45wide.png"
        #tempholder.Icon = "testImage"
        if tempholder.Center in nodelistdict.keys():
            tempnode = nodelistdict[tempholder.Center].Node
            putnode = tempnode + ', ' + tempholder.Node
            nodelistdict[tempholder.Center].Node = putnode
        else:
            nodelistdict[tempholder.Center] = tempholder

    
    
    for key in nodelistdict.keys():
        nodelist.append(nodelistdict[key])    
    #nodelist.append(tempholder)

    connectitems = []
    connectionsfile = open('/var/django/scripts/connections.dat', 'r')
    for c in connectionsfile.readlines():
        a, b = c.rstrip().split(',')
        tempholder = Holder()
        corea = Cores.objects.get(dnsname=a)
        coreb = Cores.objects.get(dnsname=b)
        lata = Coordinates.objects.get(location=corea.location).lat
        lnga = Coordinates.objects.get(location=corea.location).lng
        latb = Coordinates.objects.get(location=coreb.location).lat
        lngb = Coordinates.objects.get(location=coreb.location).lng
        coord1 = lata +', ' + lnga
        coord2 = latb +', ' + lngb
        tempholder.Coord1 = coord1
        tempholder.Coord2 = coord2
        connectitems.append(tempholder)
        lata = None
        latb = None
        


    return render_to_response('alertmap.html', {'items': nodelist, 'connectitems': connectitems})


def muxGPS(coord):
    polarity = [0,1]
    x = random.randrange(75, 150, 1)
    if len(str(x)) == 3:
        y = str('.000' + str(x))
    else:
        y = str('.0000' + str(x))
    if random.choice(polarity) == 1:
        y = str('-' + y)
    returnme = "{0:.6f}".format(float(y) + float(coord))
    return(returnme)
    


def alertjson(request):

    class Holder:
        pass
    nodelistdict = {}
    nodelist = []
    all_alerts = Alert.objects.all()
    existing_alerts = ActiveAlerts.objects.all()
    
    ea = {}
    for e in existing_alerts:
        ea[e.node] = e
    ActiveAlerts.objects.all().delete()

    for a in all_alerts:
        lat = ''
        lng = ''
        loc = a.location

        qt1 = Coordinates.objects.filter(location=loc)
        if qt1:
            locitem = Coordinates.objects.get(location=loc)
            lat = locitem.lat
            lng = locitem.lng
            #lat = str(float(lat) + .000010)
            #lng = str(float(lng) + .000010)
            lat = muxGPS(locitem.lat)
            lng = muxGPS(locitem.lng)
        else:
            continue
        tempholder = Holder()
        tempholder.Node = a.node

        if a.node in ea.keys():
            tempholder.Lat = ea[a.node].lat
            tempholder.Lng = ea[a.node].lng
        else:
            tempholder.Lat = lat
            tempholder.Lng = lng

        tempholder.Location = loc
        tempholder.Text = a.text
        tempholder.Center = tempholder.Lat + ',' + tempholder.Lng
        tempholder.Icon = "../static/Playerstatus_online.png"

        if tempholder.Center in nodelistdict.keys():
            tempnode = nodelistdict[tempholder.Center].Node
            putnode = tempnode + ', ' + tempholder.Node
            nodelistdict[tempholder.Center].Node = putnode
            new_entry = ActiveAlerts(node=putnode, lat=tempholder.Lat, lng=tempholder.Lng)
            new_entry.save()
        else:
            nodelistdict[tempholder.Center] = tempholder
            new_entry = ActiveAlerts(node=a.node, lat=tempholder.Lat, lng=tempholder.Lng)
            new_entry.save()


    for key in nodelistdict.keys():
        nodelist.append(nodelistdict[key])
    nodelist.append(tempholder)
    
    return HttpResponse(json.dumps(nodelist, default=lambda d: d.__dict__), content_type = 'application/json')



