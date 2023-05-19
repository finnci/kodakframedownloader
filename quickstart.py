from __future__ import print_function

import base64
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    service = build('gmail', 'v1', credentials=creds)

    response = service.users().messages().list(userId='me', q='has:attachment', maxResults=500).execute()
    print("Messages received - ", len(response['messages']))
    messages = response['messages']
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']

        for part in payload['parts']:
            if 'filename' in part:
                filename = part['filename']
                body = part['body']
                try:
                    data = body['attachmentId']
                except KeyError:
                    continue
                attachment = service.users().messages().attachments().get(
                    userId='me', messageId=message['id'], id=data).execute()
                file_data = base64.urlsafe_b64decode(attachment['data'])
                if filename is None or filename == "":
                    # we have to generate a file name.
                    filename = data[0:10]

                save_path = 'downloads/{}'.format(filename)
                print("Save path is -->", save_path)
                with open(save_path, 'wb') as f:
                    f.write(file_data)
                print(f"Downloaded: {filename}") 


if __name__ == '__main__':
    main()