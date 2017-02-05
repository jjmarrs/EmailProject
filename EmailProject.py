# Reorganize and delete redundant email using Gmail API
# Created by JJ Marrs

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES ='https://mail.google.com/',
'https://www.googleapis.com/auth/gmail.modify'
'https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.compose',
'https://www.googleapis.com/auth/gmail.metadata'

CLIENT_SECRET = 'client_secret.json' #Personal json file from project

''' If project is granted access, token is stored in "storage.json" file, if
    file not found then it is created and stored.'''

store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    credz = tools.run_flow(flow, store)

def main():
    service = build('gmail', 'v1', http=credz.authorize(Http()))

    #userId = user email, q = specific search query
    results = service.users().messages().list(userId = 'me', q= "from:someone@example.com").execute()

    messages = []
    if 'messages' in results:
        messages.extend(results['messages'])

    idArray = list(map(lambda x: x['id'], messages)) #stores only each email ID

    for ID in idArray: #Find each email ID and sends it to the trash bin
        service.users().messages().trash(userId = 'me', id = ID).execute()
        print("message with id " + ID + " has been trashed")

    while 'nextPageToken' in results: #Goes on to next page of email and keeps deleting
        page_token = results['nextPageToken']

        results = service.users().messages().list(userId = 'me', q = "from:someone@example.com", pageToken = page_token).execute()

        messages.extend(results['messages'])

        for ID in idArray:
            trash = service.users().messages().trash(userId = 'me', id = ID).execute()
            print("message with id " + ID + " has been trashed")

if __name__ == '__main__':
    main()
