from django import forms
from Store.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','brand','price','description','category_name','stock','is_available']

