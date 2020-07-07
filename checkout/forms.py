from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    
    class Meta:
        # Tell Django which model the form will be associated with
        model = Order
        # Specify which fields will appear on the form
        fields = ('full_name', 'email', 'phone_number',
                    'street_address1', 'street_address2',
                    'town_or_city', 'postcode', 'country',
                    'county',)
                    
                    
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated labels and set autofocus on first field
        """
        
        # Call default __init__ method to set form up as default
        super().__init__(*args, **kwargs)
        
        # Dict of placeholders to be displayed in form fields
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }
        
        # Autofocus on full_name field (cursor starts in full_name field when page is loaded)
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # Iterate through form fields
        for field in self.fields:
            # If field is required, set placeholder to field from dict and add a star to placeholder
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            # If field not required, set placeholder field from dict without star
            else:
                placeholder = placeholders[field]
                
            # Set placeholder values to their corresponding values in the dict above
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Assign css class attribute value
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Remove form field labels
            self.fields[field].label = False