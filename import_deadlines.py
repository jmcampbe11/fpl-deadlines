# Import the Fantasy Premier League JSON file
import json
import requests # TODO: Get JSON from website instead of getting it from downloaded file.

import icalendar
import datetime

import os

with open("/Users/John/Documents/download.json") as readFile:
    data = json.load(readFile)

keys = ["name", "deadline_time"]

# The "range" function's "end" parameter is exclusive.
for gameweek in list(range(0,38)):
    for key in keys:
        print(data["events"][gameweek][key])
    
# TODO: Export datetimes to .ics file.

# NOTE: "Z" suffix represents UTC

cal = icalendar.Calendar()

event = icalendar.Event()
event['dtstart'] = data["events"][gameweek]["deadline_time"]
event['dtend'] = data["events"][gameweek]["deadline_time"]
event.add('summary', data["events"][gameweek]["name"])


cal.add_component(event)

print(cal.to_ical())

print(cal.subcomponents)

# Write to .ics file
# "b" argument specifies binary mode
f = open("test.ics", "wb")
f.write(cal.to_ical())
f.close()