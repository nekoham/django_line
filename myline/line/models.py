import os
from django.db import models
from django.conf import settings
# Create your models here.

class Website(models.Model):
    url = models.CharField(max_length=200, help_text='The website\'s url for images')
    created_on = models.DateTimeField(auto_now_add=True, help_text="Date of creation")

    def __str__(self):
        return self.url
    
class Image(models.Model):
    def get_upload_to(instance, filename):
        return os.path.join(str(instance.source.id), filename)
    
    source = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='image_source')
    path = models.ImageField(upload_to=get_upload_to, help_text='The image\'s path from the website')
    created_on = models.DateTimeField(auto_now_add=True, help_text="Date of creation")

    


