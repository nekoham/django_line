import requests
from bs4 import BeautifulSoup

def scrap_get_html(url):
    r = requests.get(url=url)
    html = BeautifulSoup(r.content, 'html.parser')  
    return html              

def scrap_remove_elements(html, element):
    for href in html(element):
        href.decompose()

def scrap_get_image_data(html):
    image_data = []
    for image in html:
        tag_image = image.find("img")
        if tag_image:
            url_image = tag_image["src"]
            image_name = url_image.split('/')[7]
            image_binary = requests.get(url=url_image).content
            image_data.append([image_name, image_binary])
    return image_data