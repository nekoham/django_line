from django.views.generic import TemplateView


# Create your views here.

class IndexView(TemplateView):
    template_name = 'line/index.html'

class ListImage(TemplateView):
    template_name = 'line/images.html'

