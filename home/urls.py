# urls.py
from django.urls import path
from .views import *

app_name = "home"
urlpatterns = [
    path('', mainpage_view, name='mainpage'),
    path("license/", license_view, name="license"),
]
