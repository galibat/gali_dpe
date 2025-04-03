# views.py
from django.shortcuts import render
from django.shortcuts import redirect


def mainpage_view(request):
    return render(request, "home/mainpage.html")
