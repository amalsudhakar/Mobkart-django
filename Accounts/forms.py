from django import forms
from .models import Account, AddressBook


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Passwords do not match!'
            )
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter First Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter Last Name"
        self.fields['email'].widget.attrs['placeholder'] = "Enter Email"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Enter Phone Number"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"
            self.fields[field].widget.attrs['autocomplete'] = 'off'

class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressBook
        fields = [
            'name',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'country',
            'pincode',
            'phone',
            'status',
        ]
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = "Enter First Name"
        self.fields['address_line_1'].widget.attrs['placeholder'] = "Enter Last Name"
        self.fields['address_line_2'].widget.attrs['placeholder'] = "Enter Email"
        self.fields['city'].widget.attrs['placeholder'] = "Enter Phone Number"
        self.fields['state'].widget.attrs['placeholder'] = "Enter Phone Number"
        self.fields['country'].widget.attrs['placeholder'] = "Enter Phone Number"
        self.fields['pincode'].widget.attrs['placeholder'] = "Enter Phone Number"
        self.fields['phone'].widget.attrs['placeholder'] = "Enter Phone Number"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"