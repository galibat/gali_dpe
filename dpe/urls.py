# chemin : dpe/urls.py

from django.urls import path
from .views import *

app_name = 'dpe'

urlpatterns = [
    path("dpe_list/", dpe_list_view, name="dpe_list"),
    path("dpe_analyse/<str:ademe>/", dpe_analyse_view, name="dpe_analyse"),
    path("dpe_analyse_export_pdf/<str:ademe>/", dpe_analyse_export_pdf, name="dpe_analyse_export_pdf"),
    
]
