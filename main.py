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


def foodDay(date):
    # date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')

    # weekday = date_obj.weekday()
    # Calculate the date of next Monday
    # next_monday = date_obj + datetime.timedelta(days=7-weekday)
    # active_day = next_monday
    # r = requests.get('https://king.api.flikisdining.com/menu/api/weeks/school/king/menu-type/lunch/' + str(next_monday).split(' ')[0].split('-')[0] + '/' + str(next_monday).split(' ')[0].split('-')[1] + '/' + str(next_monday).split(' ')[0].split('-')[2] + '/')
    
    r = requests.get('https://king.api.flikisdining.com/menu/api/weeks/school/king/menu-type/lunch/' + str(date).split(' ')[0].split('-')[0] + '/' + str(date).split(' ')[0].split('-')[1] + '/' + str(date).split(' ')[0].split('-')[2] + '/')
    r = r.json()

    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    weekday = date_obj.weekday()
    weekday = (weekday+1)%7

    if len(r['days']) > 1 and len(r['days'][weekday]['menu_items']) > 3:
        active_food = r['days'][weekday]['menu_items'][3]['food']['name'] 
        createEvent(active_food,6,str(date).split(' ')[0],'12:00','12:50',False)
        # active_day = active_day + datetime.timedelta(days=1)

def populateMonth(month):
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    for i in range(days_in_month[month-1]):
        foodDay(str(datetime.datetime.now().year) + '-' + str(month) + '-' + str(i+1))

def main():
    creds = None

    if os.path.exists("token.json"):
       creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
        else:
           flow = InstalledAppFlow.from_client_secrets_file("Lunch-Menu-Calendar\credentials.json", SCOPES)
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
    populateMonth(datetime.datetime.now().month)
    print('done')