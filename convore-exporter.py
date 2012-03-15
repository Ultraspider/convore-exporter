#!/usr/bin/python

from urllib import urlopen
import json

#raw data destination
rawDataDir = "./json/"

def dumpRawData(filename, data):
   f = open(rawDataDir + filename + ".json", 'w')
   f.write(json.dumps(data))
   f.close()

#login
session = json.loads(urlopen('https://convore.com/api/account/verify.json').read())
if session.has_key('error'):
   print session['error']
   exit(-1)

print "Authentication Succesfull"
dumpRawData("me", session);

print "Gettings my groups..."
while True:
   groups = json.loads(urlopen('https://convore.com/api/groups.json').read())
   if groups.has_key('groups'):
      break;
   print "Retrying..."

print "Groups fetching done."
dumpRawData("groups", groups)

groupsID = dict([ (x['id'],x['name']) for x in groups['groups']])

for i,j in groupsID.items():
   print "Fetching Group: %s" % (j)
   print "  Getting topics..."
   while True:
      topics = json.loads(urlopen('https://convore.com/api/groups/' + i + '/topics.json').read())
      if topics.has_key('topics'):
         break
      print "  Retrying..."

   print "  Fetching of Topics done"
   dumpRawData(i + ".topics", topics)

   topicsID = dict([ (x['id'],x['name']) for x in topics['topics']])

   for k,l in topicsID.items():
      print "     Fetching content of topic: %s" % (l)
      conversation = {'messages': []}
      while True:
         LastMessages = json.loads(urlopen('https://convore.com/api/topics/' + k + '/messages.json').read())
         if LastMessages.has_key('until_id'):
            break
         print "     Retrying..."
      conversation['messages'].append(LastMessages['messages'])
      while LastMessages['until_id'] is not None:
         while True:
            LastMessages = json.loads(urlopen('https://convore.com/api/topics/' + k + '/messages.json?until_id='+ LastMessages['until_id']).read())
            if LastMessages.has_key('until_id'):
               break
            print "     Retrying..."
         conversation['messages'].insert(0, LastMessages['messages'])
      print "     Fetching of topic finished"
      dumpRawData(k + ".messages", conversation)

