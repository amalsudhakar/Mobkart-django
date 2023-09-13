from django import forms
from Store.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'brand',
                  'stock', 'is_available', 'is_delete', 'category_name']

