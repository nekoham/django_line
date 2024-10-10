from django.conf import settings
import os

def line_download_image(line_bot, image_id, image_name):
    message_content = line_bot.get_message_content(image_id).content
    path_image = os.path.join(settings.MEDIA_ROOT,'drive', image_name)
    with open(path_image, "wb") as f:
        f.write(message_content)

    return path_image