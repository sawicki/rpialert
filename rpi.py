import requests,os
import xml.etree.ElementTree as ET
from mypushover import pushover as mpo, findpath
# This program pulls an xml feed of new raspberry pi stocks
# If there are new stock numbers not in the last run, it sounds alert
ctry_list = ['US',]
rpiURL = "https://rpilocator.com/feed/"
rpiXML = requests.get(rpiURL)
rootRPI = ET.fromstring(rpiXML.text)

#prune xml tree and make a list of all xml products elements
channellevel= rootRPI.find('channel')
items = channellevel.findall('item')

# turn xml into list of lists.  Each list item contains guid, country and Title of product
new_feed = [[x.find('guid').text, x.findall('category')[1].text, x.find(
                    'title').text ] for x in items]
# get abs path to history & read. If first run, create history
guid_hist_path = findpath('guid_hist.csv')
if os.path.exists(guid_hist_path):
    with open(guid_hist_path) as f: guid_history = f.readline().split(',')
else: guid_history = [x[0] for x in new_feed]
in_ctry_list = [x for x in new_feed if x[1] in ctry_list]
new_item_list = [x[2] for x in in_ctry_list  if x[0] not in guid_history]
history_csv = ','.join([x[0] for x in new_feed])
# sound alarm with new product descriptions (pushover.net)
for i in new_item_list: mpo(i,'Sent from Digital Ocean\n'+ i,'classical')
# save new histoty file for next run          
with open(guid_hist_path,'w')as f: f.write(history_csv)
pass