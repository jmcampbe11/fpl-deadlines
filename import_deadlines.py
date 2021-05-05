# Imports the Fantasy Premier League (FPL) API JSON file
# Find JSON file at: https://fantasy.premierleague.com/api/bootstrap-static/
# Exports an .ics file that contains the FPL's Gameweek deadlines 

# TODO: Add alarm time as a function parameter

import requests
import icalendar
import re
from datetime import timedelta

# Get JSON from FPL's API
response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
data = response.json()

# Define calendar
cal = icalendar.Calendar()
cal.add("PRODID", "-//User Defined//")
cal.add("VERSION", 2.0)

keys = ["name", "deadline_time"]

# The "range" function's "end" parameter is exclusive.
for iGameweek in list(range(0,38)):
    for key in keys:
        # Add Gameweek Deadline event to calendar
        if key == "deadline_time":
            # Remove non-alphanumeric characters
            gwDeadline = re.sub(r'\W+', '', data["events"][iGameweek]["deadline_time"])

            # Create deadline event
            event = icalendar.Event()
            event['dtstart'] = gwDeadline
            event['dtend'] = gwDeadline
            event.add('summary', data["events"][iGameweek]["name"] + " Deadline")
            uid = "fpl2021-" + str(iGameweek + 1)
            event.add("UID", uid)

            # Set alarm for 2 hours before deadline
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