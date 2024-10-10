from line.api import views
from django.urls import path

urlpatterns = [
    path('webhook/', views.LineBot.as_view(), name='linewebhookdata'),
    path('image/<int:pk>/', views.DetailImageData.as_view(), name='detailimagedate'),
    path('website/<int:pk>/', views.DetailWebsiteData.as_view(), name='detailwebsitedata'),
    path('website/<int:web_id>/images/', views.ListImageData.as_view(), name='listimagedata'),
    path('website/', views.ListWebsiteData.as_view(), name='listwebsitedata')
]
