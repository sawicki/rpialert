import requests
import xml.etree.ElementTree as ET
from mypushover import pushover as mpo, findpath
# This program pulls an xml feed of new raspberry pi stocks
# If there are new stock numbers not in the last run, it sounds alert
rpiURL = "https://rpilocator.com/feed/"
rpiXML = requests.get(rpiURL)
rootRPI = ET.fromstring(rpiXML.text)

#prune xml tree and make a list of all xml products elements
channellevel= rootRPI.find('channel')
items = channellevel.findall('item')
# retrieve old product number list
historypath = findpath('history.csv')
with open(historypath) as f: history_list = f.readline().split(',')
# generate lists with new data, us stocks, items not in old list, 'new' history
us_list = [ x for x in items if x.findall('category')[1].text == 'US']
new_item_list = [x.find('title').text for x in us_list  if x.find('guid').text not in history_list]
history_list = [x.find('guid').text for x in us_list]
history_csv = ','.join(history_list)
# sound alarm with new product descriptions (pushover.net)
for i in new_item_list: mpo(i,i,'classic')
# save new histoty file for next run          
with open(historypath,'w')as f: f.write(history_csv)
pass