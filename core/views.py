from django.contrib import auth
from django.http import response
from django.shortcuts import render, redirect
from .forms import RegisterForm


def home(request):
    return render(request, 'home_page.html')


def login(request):
    context = {}
    return render(request, 'login.html', context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})
