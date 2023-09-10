from django.contrib import admin
from .models import Category, Product, Image

# Register your models here.

admin.site.register(Product)

admin.site.register(Image)

admin.site.register(Category)
