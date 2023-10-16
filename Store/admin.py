from django.contrib import admin
from .models import Category, Product, Image, Variation, VariationCategory

# Register your models here.


admin.site.register(Product)

admin.site.register(Image)

admin.site.register(Category)

admin.site.register(Variation)

admin.site.register(VariationCategory)
