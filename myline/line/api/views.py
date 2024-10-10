from io import BytesIO
import os
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
import json
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from linebot import LineBotApi
from django.conf import settings
from linebot.models import TextSendMessage
from line.models import Website, Image
from line.api.serializers import WebsiteSerializer, ImageSerializer
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.core.files.base import ContentFile
from line.services import google, line, scrap, serial
from line.api.tasks import handle_image_message, handle_text_message, handle_message

# Create your views here.

class ListWebsiteData(generics.ListAPIView):
     queryset = Website.objects.all()
     serializer_class = WebsiteSerializer

class ListImageData(generics.ListAPIView):
     serializer_class = ImageSerializer

     def get_queryset(self):
          web_id = self.kwargs.get("web_id")
          return Image.objects.filter(source=web_id)

class DetailWebsiteData(generics.RetrieveAPIView):
     queryset = Website.objects.all()
     serializer_class = WebsiteSerializer

class DetailImageData(generics.RetrieveAPIView):
     queryset = Image.objects.all()
     serializer_class = ImageSerializer

class LineBot(generics.CreateAPIView):

     def post(self, request, *args, **kwargs):
          # line_bot_api = LineBotApi(settings.LINE_TOKEN)

          handle_message.delay(request.data)
          return Response({'message': 'Handling the message'}, status=status.HTTP_200_OK) 

     # def post(self, request, *args, **kwargs):          
     #      # Create variables for each data from the message
     #      data = request.data
     #      data_event = data['events'][0]
     #      message_type = data_event['message']['type']
     #      reply_token = data_event['replyToken']

     #      # It's a text message, take the URL to scrap pictures and save them in database
     #      if message_type == 'text':
     #           url = data_event['message']['text']
     #           handle_text_message.delay(url, reply_token)
     #           return Response('Handling the text message', status=status.HTTP_200_OK)
     #           # validator = URLValidator()
     #           # try:
     #           #      validator(url)

     #           #      # Get the whole page's html
     #           #      html = scrap.scrap_get_html(url)

     #           #      # Remove all unneeded elements that might pass the finding filter
     #           #      scrap.scrap_remove_elements(html, "a")

     #           #      div_image = html.find("div", {"id": "readerarea"}).find_all("p")

     #           #      # Find and get all image's names and data
     #           #      image_data = scrap.scrap_get_image_data(div_image)

     #           #      # Save the website URL to database
     #           #      web_instance = serial.serial_save_website(url)

     #           #      # Save all images from the url to database
     #           #      for image_name, image_binary in image_data:
     #           #           serial.serial_save_image(web_instance, image_binary, image_name)
                    
     #           #      line_bot_api.reply_message(reply_token, TextSendMessage(text="Your URL and images have been successfully received."))

     #           #      return Response({'message': 'URL and images successfully received'}, status=status.HTTP_200_OK)   
     #           # except ValidationError:
     #           #      line_bot_api.reply_message(reply_token, TextSendMessage(text="Sorry, the URL you sent is not a valid HTTPS URL."))
     #           #      return Response({'Error': 'Not valid URL'}, status=status.HTTP_400_BAD_REQUEST)
               
     #      # It's an image, download it and save it to google drive.
     #      elif message_type == 'image':

     #           image_id = data_event['message']['id']

     #           handle_image_message.delay(image_id, reply_token)
     #           return Response('Handling the text message', status=status.HTTP_200_OK)

     #           # image_name = image_id + ".png"
               
     #           # # Download image from message and get path
     #           # image_path = line.line_download_image(line_bot_api, image_id, image_name)

     #           # # Auth and get google auth
     #           # gauth = google.google_auth()

     #           # # Use google auth to upload an image to google drive  
     #           # google.google_upload(gauth, image_name, image_path)           
               
     #           # line_bot_api.reply_message(reply_token, TextSendMessage(text="Your image has been successfully received."))
               
     #           # return Response({'message': 'Image successfully received'}, status=status.HTTP_200_OK) 
     