from django.contrib import auth
from django.http import response, HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'home_page.html')


def product_one(request):
    return render(request, 'product/product1.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Incorrect username or passworh')
    context = {}
    return render(request, 'account/login.html', context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for' + '' + user)
        return redirect('/')
    else:
        form = RegisterForm()
    context = {"form": form}
    return render(request, "account/register.html", context)
