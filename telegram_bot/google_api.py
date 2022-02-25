from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']


def auth():
    """ Авторизация google """
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            url = flow.authorization_url()
            return url


def calendar_event(creds):
    """ Список задач на текущий день из календаря """
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    tomorrow = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events


if __name__ == '__main__':
    print()
