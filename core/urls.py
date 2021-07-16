from django.urls import path
from .views import home, loginPage, register, product_one

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginPage, name='login'),
    path('register/', register, name='register'),
    path('product_one/', product_one, name='product_one'),
]
