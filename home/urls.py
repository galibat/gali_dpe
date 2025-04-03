# urls.py
from django.urls import path
from .views import mainpage_view

app_name = "home"
urlpatterns = [
    path('', mainpage_view, name='mainpage'),
]
