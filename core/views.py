from django.views.generic import ListView, DeleteView, View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import response, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.detail import DetailView
from .forms import RegisterForm, CheckOutForm
from .models import Item, OrderItem, Order, Address, Coupon


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


def about_us(request):
    return render(request, 'about_us.html')


def our_service(request):
    return render(request, 'our_service.html')


def after_care(request):
    return render(request, 'after_care.html')


def our_work(request):
    return render(request, 'our_work.html')


def contact(request):
    return render(request, 'contact.html')


class HomeView(ListView):
    model = Item
    template_name = 'home_page.html'


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product/product1.html'


class ShopDetailView(ListView):
    model = Item
    template_name = 'Shop.html'


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome Back {request.user}")
            return redirect('/')
        else:
            messages.warning(request, 'Incorrect username or password')
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


@login_required
def add_to_cart(request, slug):
    # get item
    item = get_object_or_404(Item, slug=slug)
    # get or create the object item to the OrderItem model
    order_item, created = OrderItem.objects.get_or_create(
        user=request.user,
        item=item,
        ordered=False
    )
    # check if user in order model got order query
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    # if order query exist
    if order_qs.exists():
        order = order_qs[0]
        # if item exist in order query, add quantity
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect('/order_summary')
        # else add item to order query
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('/order_summary')
    # else create new order for user
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('/order_summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                user=request.user,
                item=item,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect('/order_summary')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('/')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('/')


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                user=request.user,
                ordered=False,
                item=item
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            return redirect('/order_summary')
        else:
            return redirect('/')
    else:
        return redirect('/')


class OrderSummaryView(LoginRequiredMixin, View):  # def orderSummaryView(request)
    def get(self, *args, **kwargs):  # if request.method == 'GET'
        try:
            # get order qs
            order = Order.objects.get(
                user=self.request.user,
                ordered=False
            )
            context = {
                'order': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('/')


class CheckOutView(View):
    def get(self, *args, **kwargs):  # If request.method == 'GET'
        try:
            order = Order.objects.get(
                user=self.request.user,
                ordered=False
            )
            form = CheckOutForm()
            context = {
                'form': form,
                'order': order
            }
            return render(self.request, 'checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order.')
            return redirect('/checkout')

    def post(self, *args, **kwargs):  # If request.method == 'POST'
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(
                user=self.request.user,
                ordered=False
            )
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping'
                )
                if use_default_shipping:
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, 'No default shipping address available.')
                        return redirect('/checkout')
                else:
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_city = form.cleaned_data.get('shipping_city')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')
                    shipping_states = form.cleaned_data.get('shipping_states')
                    if is_valid_form([shipping_address1, shipping_city, shipping_country, shipping_zip, shipping_states]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            city=shipping_city,
                            country=shipping_country,
                            zip=shipping_zip,
                            states=shipping_states
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = (
                            form.cleaned_data.get('set_default_shipping')
                        )
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(
                            self.request, 'Please fill in the required shipping address fields')
                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == 'S':
                    return redirect('/payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('/payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, 'Invalid payment option selected.')
                    return redirect('/checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order.')
            return redirect('/order_summary')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(
            user=self.request.user,
            ordered=False
        )
        context = {
            'order': order,
        }
        return render(self.request, 'checkout.html', context)
