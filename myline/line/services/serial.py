from line.api.serializers import WebsiteSerializer, ImageSerializer
from django.core.files.base import ContentFile


def serial_save_website(url):
    web_data = {"url": url, "image_source": []}
    web_serializer = WebsiteSerializer(data=web_data)
    if web_serializer.is_valid():
        return web_serializer.save()
    return web_serializer.errors


def serial_save_image(web_instance, image_binary, image_name):
    image_data = {"source": web_instance.pk, "path": ContentFile(image_binary, image_name)}
    image_serializer = ImageSerializer(data=image_data)
    if image_serializer.is_valid():
        image_serializer.save()
    return image_serializer.errors