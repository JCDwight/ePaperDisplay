#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import print_function

import sys
import os
from datetime import datetime
import os.path
import logging
import time
from turtle import width
from PIL import Image,ImageDraw,ImageFont
import traceback
import platform as plat
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def CheckPlatform():
    #Checks the platform the program is running on.  Linux = 1, Windows = 2, everything else is 3
    if (plat.platform()[0] == "L" or plat.platform()[0] == "l"):
        return 1
    elif (plat.platform()[0] == "W" or plat.platform()[0] == "w"):
        return 2
    else:
        return 3


logging.basicConfig(level=logging.DEBUG)




picdir = 'pic'
libdir = 'lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

# Function to return ordinal suffix for day of the month
def get_ordinal(n):
    if 4 <= n <= 20 or 24 <= n <= 30:
        return str(n) + "th"
    else:
        return str(n) + {1: "st", 2: "nd", 3: "rd"}[n % 10]


if (CheckPlatform() == 1):
    from waveshare_epd import epd7in5b_V2
    print('Imported Waveshare')
elif (CheckPlatform() == 2):
    pass

def ePaperDemo():

    try:
        logging.info("epd7in5b_V2 Demo")
        epd = epd7in5_V2.EPD()
    
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        font96 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 96)
        font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 3 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=3, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])
            print(events)
            print(type(events))
            if not events:
                print('No upcoming events found.')
                return
            print("")
            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print (event)
                print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)


        #draw.rectangle((1,1,479,275))
        draw.rectangle((0,0,480,275),width = 5, outline= 0)
        start = events[0]['start'].get('dateTime', events[0]['start'].get('date'))
        date = datetime.strptime(start, "%Y-%m-%d")
        formatted = date.strftime("%a, (%b, %d) - ")
        formatted2 = str(events[0]['summary'])
        draw.text((20, 20), formatted, font = font48, fill = 0)
        draw.text((100, 120), formatted2, font = font48, fill = 0)
        draw.rectangle((0,275,480,550),width = 5, outline= 0)        
        start = events[1]['start'].get('dateTime', events[1]['start'].get('date'))
        date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
        formatted = date.strftime("%a, (%b, %d) - ")
        formatted2 = str(events[1]['summary'])
        draw.text((20, 295), formatted, font = font48, fill = 0)
        draw.text((100, 395), formatted2, font = font48, fill = 0)
        draw.rectangle((0,275,480,550),width = 5, outline= 0)
        start = events[2]['start'].get('dateTime', events[2]['start'].get('date'))
        date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
        formatted = date.strftime("%a, (%b, %d) - ")
        formatted2 = str(events[2]['summary'])
        draw.text((20, 570), formatted, font = font48, fill = 0)
        draw.text((100, 670), formatted2, font = font48, fill = 0)       
        draw.rectangle((0,550,480,800),width = 5, outline= 0)
    
        epd.display(epd.getbuffer(Limage))
        time.sleep(2)

        logging.info("Goto Sleep...")
        epd.sleep()
    
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5_V2.epdconfig.module_exit()
        exit()

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    ePaperDemo()
    exit()
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=3, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)




if __name__ == '__main__':
    main()