from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name','phone','email','address_line_1','address_line_2','country','state','city','order_note','pincode']
        
        def __init__(self, *args, **kwargs):
            super(OrderForm, self).__init__(*args, **kwargs)
            self.fields['name'].widget.attrs['placeholder'] = "Enter First Name"
            self.fields['phone'].widget.attrs['placeholder'] = "Enter Phone Number"
            self.fields['email'].widget.attrs['placeholder'] = "Enter Email"
            self.fields['address_line_1'].widget.attrs['placeholder'] = "Enter Address"
            self.fields['address_line_2'].widget.attrs['placeholder'] = "Enter Address(optional)"
            self.fields['country'].widget.attrs['placeholder'] = "Enter country"
            self.fields['state'].widget.attrs['placeholder'] = "Enter state"
            self.fields['city'].widget.attrs['placeholder'] = "Enter city"
            self.fields['order_note'].widget.attrs['placeholder'] = "Enter order note"
            self.fields['pincode'].widget.attrs['placeholder'] = "Enter pincode"
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = "form-control"
                self.fields[field].widget.attrs['autocomplete'] = 'off'