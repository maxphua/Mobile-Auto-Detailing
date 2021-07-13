from django.urls import path
from .views import home, login, register

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register')
]
