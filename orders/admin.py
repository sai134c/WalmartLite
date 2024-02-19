from django.contrib import admin
from .models import Order, OrderElement

admin.site.register(Order)
admin.site.register(OrderElement)
