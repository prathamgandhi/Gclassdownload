from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.announcements.readonly',
          'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly']


def main():
    start = time.time()
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)
    # Calling API to check for announcements
    results_maths = service.courses().announcements().list(courseId='239126584699', pageSize=4).execute()
    announcements_maths = results_maths.get('announcements', [])


''' results_bee = service.courses().announcements().list(courseId='242646217643', pageSize=1).execute()
    announcements_bee = results_bee.get('announcements', [])
    results_comm = service.courses().announcements().list(courseId='239645079891', pageSize=1).execute()
    announcements_comm = results_comm.get('announcements', [])
    results_phy = service.courses().announcements().list(courseId='211434499442', pageSize=1).execute()
    announcements_phy = results_phy.get('announcements', [])
    results_chem = service.courses().announcements().list(courseId='239601565740', pageSize=1).execute()
    announcements_chem = results_chem.get('announcements', [])'''




'''    if not announcements:
        print('No courses found.')
    else:
        print('Courses:')
        for announcement in announcements:
            print(announcement['text'])
            print(announcement['updateTime'])
'''

if __name__ == '__main__':
    main()
