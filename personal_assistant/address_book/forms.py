from django import forms
from django.core.exceptions import ValidationError

from .models import AddressBook


class AddressBookForm(forms.ModelForm):

    class Meta:
        model = AddressBook
        fields = ['first_name', 'last_name', 'address', 'phone', 'email', 'birthday']

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']

        if not phone_number.isdigit():
            raise ValidationError("Phone number should contain only digits.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email.endswith('@example.com'):
            raise ValidationError("Invalid email address.")
        return email


class SearchContactForm(forms.Form):
    query = forms.CharField(min_length=3, max_length=32, required=False, initial='')

class DeleteContactForm(forms.Form):
    contact_id = forms.IntegerField(widget=forms.HiddenInput())