from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.conf import settings

def google_auth():
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("creds.json")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("creds.json")

    return gauth

def google_upload(gauth, image_name, image_path):
    drive = GoogleDrive(gauth)
    df = drive.CreateFile({'parents': [{"id": settings.DRIVE_ID}], "title": image_name, }) 
    df.SetContentFile(image_path) 
    df.Upload() 

