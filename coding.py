# from simplegmail import Gmail

# gmail = Gmail()

# # Unread messages in your inbox
# try: 
#     messages = gmail.get_starred_messages()
# except:
#     print('here')
# # Starred messages


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "client_secret.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")

    for label in labels:
      print(label["name"])
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/parsingmails/topics/paperless',
        'labelFilterBehavior': 'INCLUDE'
    }

    
    # res = service.users().watch(userId='me', body=request).execute()
    # exit(0)

    # cos = 4142222
    # res2 = service.users().history().list(userId='me', startHistoryId = '4142519').execute()
    # print(res2)

    # # res1 = service.users().messages().get(userId='me', id = "18d08a5fafd19f9e").execute()
    # # print(res1)
    # exit(0)
    res2 = service.users().messages().get(userId='me', id = "18d2762a6ee439ef").execute()
    # print(res1)
    # print(res2['payload']['parts'])
    for part in res2['payload']['parts']:
      if part['filename']:
        print(part)
        att = service.users().messages().attachments().get(userId="me", messageId="18d2762a6ee439ef",id=part['body']['attachmentId']).execute()
        file_data = base64.urlsafe_b64decode(att['data'].encode('UTF-8'))
        with open(part['filename'], 'wb') as f:
            f.write(file_data)
    
    # print(res2)
    # for history in res2['history']:
    #   res1 = service.users().messages().get(userId='me', id = history['messages'][0][]).execute()
    #   print(res1)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()