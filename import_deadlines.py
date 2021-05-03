# Import the Fantasy Premier League (FPL) JSON file
# Exports an .ics file that contains the FPL's Gameweek deadlines 

import json
#import requests # TODO: retrieve JSON from website instead of downloaded file.
import icalendar
from datetime import timedelta
import os
import re

with open("/Users/John/Documents/download.json") as readFile:
    data = json.load(readFile)

# Define calendar
cal = icalendar.Calendar()
cal.add("PRODID", "-//User Defined//")
cal.add("VERSION", 2.0)

keys = ["name", "deadline_time"]

# The "range" function's "end" parameter is exclusive.
for iGameweek in list(range(0,38)):
    for key in keys:
        print(data["events"][iGameweek][key])
        # Add Gameweek Deadline event to calendar
        if key == "deadline_time":
            # Remove non-alphanumeric characters
            gwDeadline = re.sub(r'\W+', '', data["events"][iGameweek]["deadline_time"])

            event = icalendar.Event()
            event['dtstart'] = gwDeadline
            event['dtend'] = gwDeadline
            event.add('summary', data["events"][iGameweek]["name"] + " Deadline")
            # add gw number to UID
            uid = "fpl2021-" + str(iGameweek + 1)
            event.add("UID", uid)

            # Simple Calendar Specific 
            event.add("CATEGORY_COLOR", -16452352)
            #event.add("CATEGORIES", "Reminder") # iCalendar formats stirng as - R,e,m,i,n,d,e,r

            # TODO: Add alarm (2 hours before event)

            alarm = icalendar.Alarm()
            alarm.add("ACTION", "DISPLAY")
            alarmDelta = timedelta(hours = -2)
            alarm.add("TRIGGER", alarmDelta)
            alarm.add("DESCRIPTION", "Reminder")

            event.add_component(alarm)

            cal.add_component(event)

# Write to .ics file
f = open("FPL_GW_Deadlines.ics", "wb")
f.write(cal.to_ical())
f.close()

# TODO: add code to Github


