from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.shortcuts import reverse, redirect
from django.conf import settings
from django_countries.fields import CountryField

CATEGORY_CHOICES = (
    ('V', 'VOUCHERS'),
    ('P', 'PACKAGES')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product_one", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('core:add_to_cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('core:remove_from_cart', kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f" {self.quantity} of {self.item}"

    def get_total_item_price(self):
        return self.item.price * self.quantity

    def get_total_discount_item_price(self):
        return self.item.discount_price * self.quantity

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    ordered_date = models.DateTimeField()
    shipping_address = models.ForeignKey(
        'Address', related_name='Shipping_address', on_delete=models.SET_NULL, blank=True, null=True
    )
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    states = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    contact_name = models.CharField(max_length=15)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    messages = models.TextField()

    def __str__(self):
        return self.contact_name
