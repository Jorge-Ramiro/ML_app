import os
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

def logging():
    creds = None
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    if os.path.exists('GoogleDrive_API_connections/token.json'):
        creds = Credentials.from_authorized_user_file('GoogleDrive_API_connections/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'GoogleDrive_API_connections/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('GoogleDrive_API_connections/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def search_files(query="mimeType='application/x-zip-compressed'"):
    creds = logging()
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = service.files().list(q=query,
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                    'files(id, name)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                print(F'Found file: {file.get("name")}, {file.get("id")}')
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None
    return files


def upload_file(file_path, folder_id="1aaUczscHtbG68VRSgZR5VkF9pR1nB_JW"):
    title = file_path.split('/')[-1]
    creds = logging()
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {
            'name': title,
            'parents': [folder_id]}
        media = MediaFileUpload(title, resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                        fields='id').execute()
        print(F'File ID: "{file.get("id")}".')
        return file.get('id')
    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def download_file(name_file, path="./"):
    creds = logging()
    file_found = search_file(name_file)
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_found['id'])
        file = io.FileIO(path + file_found['name'], mode='wb')
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print("Download %d%%." % int(status.progress() * 100))
            print("Download Complete!")
    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None
        print("Entro al except")
    finally:
        file.close()


def search_file(title):
    creds = logging()
    try:
        service = build('drive', 'v3', credentials=creds)
        file = {}
        page_token = None
        response = service.files().list(q=f"name='{title}'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                    'files(name, id, mimeType)',
                                            pageToken=page_token).execute()
        for file in response.get('files', []):
            file = file
    except HttpError as error:
        print(f'An error occurred: {error}')
        file = None
    return file



if __name__=="__main__":
    import requests
    #logging()
    file_path = "./new_user_credentials.csv"
    #upload_file(file_path)
    id = "16QXPDPk0gQqUCN4kJzYD1Ntct4XPMvwF"
    name = "winequality.zip"
    #search_files()
    #download_file(name, id)
    #search_file()
    download_file(name, "../GD_connection/")

