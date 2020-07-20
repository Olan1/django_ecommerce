from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        # Tell Django which model the form will be associated with
        model = UserProfile
        
        exclude = ('user', )
                    
                    
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated labels and set autofocus on first field
        """
        
        # Call default __init__ method to set form up as default
        super().__init__(*args, **kwargs)
        
        
        # Dict of placeholders to be displayed in form fields
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }
        
        # Autofocus on full_name field (cursor starts in full_name field when page is loaded)
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        # Iterate through form fields
        for field in self.fields:
            if field != 'default_country':
                # If field is required, set placeholder to field from dict and add a star to placeholder
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                # If field not required, set placeholder field from dict without star
                else:
                    placeholder = placeholders[field]
                    
                # Set placeholder values to their corresponding values in the dict above
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Assign css class attribute value
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            # Remove form field labels
            self.fields[field].label = False
