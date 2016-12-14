#!/usr/bin/python3
import requests
import re
import json
import html

'''
Logs in to portal.fhict.nl
Tries to read submissions 2..251, doesn't give a fuck if one fails
Does some shady string operations and summons zalgo
Writes what everyone voted to results.json
'''


headers = {
    'Host': 'portal.fhict.nl',
    # Set a nice user agent to explain to friendly worried sysadmins why a single client did 252 requests in a few seconds
    'User-Agent': 'bef0re\'s robot counting the votes on NEXT week subjects (GitHub version)',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Content-Length': '0',
}

s = requests.session()
s.headers.update(headers)

# Log in

data = {
    "curl": "Z2F",
    "flags": 0,
    "forcedownlevel":0,
    "formdir": 6,
    "username": "",     # Insert your portal.fhict.nl username here
    "password": "",     # Insert your portal.fhict.nl password here
    "trusted":0,
    "SubmitCreds":"Log+On",
}

print ("Logging in...")
r = s.post("https://portal.fhict.nl/CookieAuth.dll?Logon",data=data)

ballots = {}
for i in range(2,252):
    print ("Requesting page "+str(i))
    r = s.post('https://portal.fhict.nl/Studentenplein/Lists/NEXTSubjects/DispForm.aspx?ID='+str(i))

    # Cut away everything before and after what we want
    start = '<table class="ms-formtable" style="margin-top: 8px;" border="0" cellpadding="0" cellspacing="0" width="100%">'
    end = '<tr id="idAttachmentsRow">'

    text = r.text[r.text.find(start):r.text.find(end)]

    # Get rid of newlines and tabs
    text = text.replace("\r\n","")
    text = text.replace("\t","")

    # Decode htmlentities
    text = html.unescape(text)

    # Then pick out what we want and summon zalgo at the same time
    groups =  re.findall('-->(.*?)</td>', text)

    '''
    groups[0]           workshops
    groups[1][43:-12]   workshops_textbox
    groups[2]           gastsprekers
    groups[3][43:-12]   gastsprekers_textbox
    groups[4]           entertainment
    groups[5][43:-12]   entertainment_textbox

    [43:-12] cuts away some dirt, ehhh HTML.
    '''

    try:
        ballots[i] = {}
        ballots[i]['workshops'] = groups[0].split('; ')
        ballots[i]['workshops_textbox'] = groups[1][43:-12]
        ballots[i]['gastsprekers'] = groups[2].split('; ')
        ballots[i]['gastsprekers_textbox'] = groups[3][43:-12]
        ballots[i]['entertainment'] = groups[4].split('; ')
        ballots[i]['entertainment_textbox'] = groups[5][43:-12]
    except IndexError:
        print ("Warning: page " + str(i) + " gave an IndexError")
        # parsing didn't work.

        # To prevent gastsprekers from leaking into entertainment, we need to cleanse this ballot
        ballots[i] = {}


print ("Writing everything to results.json:")
with open("results.json",'w') as f:
    print (json.dumps(ballots), file=f)
