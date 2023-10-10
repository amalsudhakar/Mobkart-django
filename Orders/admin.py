from django.contrib import admin
from Orders.models import Order, OrderProduct, Payment

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Payment)