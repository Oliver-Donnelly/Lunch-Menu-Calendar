import os.path
import datetime
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def createEvent(title, color, date, startTime, endTime, allDay):

    event = {
        "summary": title,
        "colorId": color,
        "start": {
            "date": date if allDay else None,
            "dateTime": None if allDay else date + 'T' + startTime + ':00',
            "timeZone": 'America/New_York'
            },
        "end": {
            "date": date if allDay else None,
            "dateTime": None if allDay else date + 'T' + endTime + ':00',
            "timeZone": 'America/New_York'
            }
    }
    event = service.events().insert(calendarId="primary",body=event).execute()


def populateWeek(date):
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')

    weekday = date_obj.weekday()
    # Calculate the date of next Monday
    days_until_monday = (7 - weekday) % 7
    next_monday = str(date_obj + datetime.timedelta(days=days_until_monday))
    r = requests.get('https://king.api.flikisdining.com/menu/api/weeks/school/king/menu-type/lunch/' + next_monday.split(' ')[0].split('-')[0] + '/' + next_monday.split(' ')[0].split('-')[1] + '/' + next_monday.split(' ')[0].split('-')[2] + '/')
    r = r.json()
    for i in range(5):
        day1Food = r['days'][1+i]['menu_items'][3]['food']['name']
        print(day1Food)

def main():
    creds = None

    if os.path.exists("token.json"):
       creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
        else:
           flow = InstalledAppFlow.from_client_secrets_file("Weather-on-Calendar/credentials.json", SCOPES)
           creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        global service
        service = build("calendar", "v3", credentials=creds)

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    main()
    # createEvent('Test Event for septemeber 14', 6,'2024-9-15', '10:30', '11:00', True)
    populateWeek('2024-9-7')