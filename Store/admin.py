from django.contrib import admin
from .models import Category, Product, Image

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category',)}
    list_display = ('category', 'slug')

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','category_name','brand','price','created_date')
    prepopulated_fields = {'slug' : ('product_name',)}

admin.site.register(Product, ProductAdmin)

admin.site.register(Image)
