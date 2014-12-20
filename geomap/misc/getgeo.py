#!/usr/bin/local

import requests
import json




def citySet(c):
    return {
            'city' : 'cityname',
            }.get(c, 'city')





def geoCode(location, city='cityname'):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    locationplus = location.replace(' ','+')
    setcity = citySet(city)
    locationstring = locationplus + '+' + setcity + '+STATECODE&sensor=false'
    response = requests.get(url + locationstring)
    a = response.text
    response_text = json.loads(a.encode('ascii'))
    lat = response_text['results'][0]['geometry']['location']['lat']
    lng = response_text['results'][0]['geometry']['location']['lng']
    return(lat, lng)




