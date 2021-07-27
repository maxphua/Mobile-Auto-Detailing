from django.urls import path
from .views import HomeView, loginPage, register, ProductDetailView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', loginPage, name='login'),
    path('register/', register, name='register'),
    path('product_one/<slug>', ProductDetailView.as_view(), name='product_one'),
]
