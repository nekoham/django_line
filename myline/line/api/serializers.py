from rest_framework import serializers
from line.models import Website, Image

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id', 'url', 'created_on']
    

class ImageSerializer(serializers.ModelSerializer):
    source_detail = WebsiteSerializer(source = 'source', read_only=True)
    class Meta:
        model = Image
        fields = ['source_detail', 'source', 'id', 'path']


    
