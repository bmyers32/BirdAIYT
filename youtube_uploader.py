
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YouTubeUploader:
    def __init__(self, secrets_file):
        self.secrets_file = secrets_file
        self.service = self.get_authenticated_service()

    def get_authenticated_service(self):
        scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        flow = InstalledAppFlow.from_client_secrets_file(self.secrets_file, scopes)
        creds = flow.run_console()
        return build("youtube", "v3", credentials=creds)

    def upload(self, file_path, title, description, tags):
        request = self.service.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=MediaFileUpload(file_path)
        )
        return request.execute()
