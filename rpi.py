from os.path import exists
import requests
import xml.etree.ElementTree as ET
# import os
# from twilio.rest import Client
from mypushover import pushover as mpo, findpath
from pprint import pprint

# history file is "history.csv" containds element ids from previous run



rpiURL = "https://rpilocator.com/feed/"
rpiXML = requests.get(rpiURL)

rootRPI = ET.fromstring(rpiXML.text)

#prune xml tree and make a list of all xml products
channellevel= rootRPI.find('channel')
items = channellevel.findall('item')
# 
historypath = findpath('history.csv')
with open(historypath) as f: history_list = f.readline().split(',')
 
us_list = [ x for x in items if x.findall('category')[1].text == 'US']
new_item_list = [x.find('title').text for x in us_list  if x.find('guid').text not in history_list]
history_list = [x.find('guid').text for x in us_list]
history_csv = ','.join(history_list)
for i in new_item_list: mpo(i,i,'classic')
            
with open(historypath,'w')as f: f.write(history_csv)
        
pass