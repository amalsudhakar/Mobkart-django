from django.contrib import admin
from .models import Category, Product, Image, Variation, VariationCategory, ProductCategoryConnection

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category_name', 'stock']

admin.site.register(Product,ProductAdmin)

admin.site.register(Image)

admin.site.register(Category)

class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'stock']


admin.site.register(Variation, VariationAdmin)

admin.site.register(VariationCategory)

class ProductCategoryConnectionAdmin(admin.ModelAdmin):
    list_display = ['product']

admin.site.register(ProductCategoryConnection, ProductCategoryConnectionAdmin)
