# import requests
import json,os
import xml.etree.ElementTree as ET
import http.client, urllib

# Send the push/message to all devices connected to Pushbullet
# use from mypushover import * in main program
def pushover(title,message,sound='pushover'):
    filepath = findpath('pushoverauth.txt')
    # with open(filepath) as f:
    #     passcsv = f.readline()
    #     myuser, mytoken =  passcsv.split(',')
    passcsv = os.getenv('PUSHOVER')
    myuser, mytoken =  passcsv.split(',')
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": mytoken,
            "user": myuser,
            "title":title,
            "message":message,
            "sound":sound
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    
    # messageData = 'token='+mytoken+'&user='+myuser+'&title='+'rpilocator Stock Alert'
    # message = messageData+'&message='+title+'&url='+link
    # req = requests.post(url='https://api.pushover.net/1/messages.json', data=message, timeout=20)

def findpath(filename):
    dn = os.path.dirname(os.path.realpath(__file__))
    mypath = os.path.join(dn, filename)
    return mypath