from django.urls import path
from . import views

app_name = "line"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("website/<int:pk>/images", views.ListImage.as_view(), name="listimage")
]
