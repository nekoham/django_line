from time import sleep
from celery import shared_task
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from linebot.models import TextSendMessage
from line.services import google, line, scrap, serial
from linebot import LineBotApi
from django.conf import settings
import os

@shared_task
def handle_text_message(url, reply_token):
    line_bot_api = LineBotApi(settings.LINE_TOKEN)
    try:
        validator = URLValidator()
        validator(url)

        # Get the whole page's html
        html = scrap.scrap_get_html(url)

        # Remove all unneeded elements that might pass the finding filter
        scrap.scrap_remove_elements(html, "a")

        div_image = html.find("div", {"id": "readerarea"}).find_all("p")

        # Find and get all image's names and data
        image_data = scrap.scrap_get_image_data(div_image)

        # Save the website URL to database
        web_instance = serial.serial_save_website(url)

        # Save all images from the url to database
        for image_name, image_binary in image_data:
                serial.serial_save_image(web_instance, image_binary, image_name)
        
        line_bot_api.reply_message(reply_token, TextSendMessage(text="Your URL and images have been successfully received."))
        return {'message': 'URL and images successfully received', 'status':'status.HTTP_200_OK'}
    
    except ValidationError:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="Sorry, the URL you sent is not a valid HTTPS URL."))
        return {'Error': 'Not valid URL', 'status':'status.HTTP_400_BAD_REQUEST'}
    

@shared_task
def handle_image_message(image_id, reply_token):
    line_bot_api = LineBotApi(settings.LINE_TOKEN)

    image_name = image_id + ".png"
    
    # Download image from message and get path
    image_path = line.line_download_image(line_bot_api, image_id, image_name)

    # Auth and get google auth
    gauth = google.google_auth()

    # Use google auth to upload an image to google drive  
    google.google_upload(gauth, image_name, image_path)           
    os.remove(image_path)

    line_bot_api.reply_message(reply_token, TextSendMessage(text="Your image has been successfully received."))
    return {'message': 'Image successfully received', 'status':'status.HTTP_200_OK'}
    

@shared_task
def handle_message(data):
    line_bot_api = LineBotApi(settings.LINE_TOKEN)

    # Create variables for each data from the message
    data_event = data['events'][0]
    message_type = data_event['message']['type']
    reply_token = data_event['replyToken']

    # It's a text message, take the URL to scrap pictures and save them in database
    if message_type == 'text':
        url = data_event['message']['text']
        validator = URLValidator()
        try:
             validator(url)

             # Get the whole page's html
             html = scrap.scrap_get_html(url)

             # Remove all unneeded elements that might pass the finding filter
             scrap.scrap_remove_elements(html, "a")

             div_image = html.find("div", {"id": "readerarea"}).find_all("p")

             # Find and get all image's names and data
             image_data = scrap.scrap_get_image_data(div_image)

             # Save the website URL to database
             web_instance = serial.serial_save_website(url)

             # Save all images from the url to database
             for image_name, image_binary in image_data:
                  serial.serial_save_image(web_instance, image_binary, image_name)
            
             line_bot_api.reply_message(reply_token, TextSendMessage(text="Your URL and images have been successfully received."))

             return {'message': 'URL and images successfully received', 'status':'status.HTTP_200_OK'}
        except ValidationError:
             line_bot_api.reply_message(reply_token, TextSendMessage(text="Sorry, the URL you sent is not a valid HTTPS URL."))
             return {'Error': 'Not valid URL', 'status':'status.HTTP_400_BAD_REQUEST'}
        
    # It's an image, download it and save it to google drive.
    elif message_type == 'image':

        image_id = data_event['message']['id']
        image_name = image_id + ".png"
        
        # Download image from message and get path
        image_path = line.line_download_image(line_bot_api, image_id, image_name)

        # Auth and get google auth
        gauth = google.google_auth()

        # Use google auth to upload an image to google drive  
        google.google_upload(gauth, image_name, image_path)           
        
        line_bot_api.reply_message(reply_token, TextSendMessage(text="Your image has been successfully received."))
        
        return {'message': 'Image successfully received', 'status':'status.HTTP_200_OK'}