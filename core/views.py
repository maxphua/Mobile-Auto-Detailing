from django.shortcuts import render
from django.views.generic import View, ListView


def home(request):
    return render(request, 'home_page.html')
