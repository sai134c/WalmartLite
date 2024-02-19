from django.db import models
from shopApp.models import Product
from django.contrib.auth.models import User
from orders.models import Order
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    date_of_birth = models.DateField()
    payment_card = models.CharField(max_length=16)
    Walmart_cash = models.DecimalField(max_digits=13,decimal_places=2, validators=[MinValueValidator])
    cart = models.ManyToManyField(Product)
    address = models.TextField(max_length=250)
    phone_number = PhoneNumberField(blank = True)
    order_history = models.ManyToManyField(Order)



