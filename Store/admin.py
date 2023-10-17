from django.contrib import admin
from .models import Category, Product, Image, Variation, VariationCategory

# Register your models here.


admin.site.register(Product)

admin.site.register(Image)

admin.site.register(Category)

class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'stock']


admin.site.register(Variation, VariationAdmin)

admin.site.register(VariationCategory)
