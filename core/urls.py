from django.urls import path
from .views import (
    HomeView,
    about_us,
    our_service,
    after_care,
    our_work,
    contact,
    OrderSummaryView,
    loginPage,
    register,
    ProductDetailView,
    ShopDetailView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    OrderSummaryView,
    CheckOutView,
    PaymentView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about_us/', about_us, name='about_us'),
    path('our_service/', our_service, name='our_service'),
    path('after_care/', after_care, name='after_care'),
    path('our_work/', our_work, name='our_work'),
    path('contact/', contact, name='contact'),
    path('login/', loginPage, name='login'),
    path('register/', register, name='register'),
    path('product_one/<slug>', ProductDetailView.as_view(), name='product_one'),
    path('shop/', ShopDetailView.as_view(), name='shop'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>/',
         remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('order_summary/', OrderSummaryView.as_view(), name='summary_view'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment')
]
