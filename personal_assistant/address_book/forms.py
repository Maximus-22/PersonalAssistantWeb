from django import forms
from django.core.exceptions import ValidationError

from .models import AddressBook


class AddressBookForm(forms.ModelForm):
    tags = forms.CharField(max_length=84, help_text="To create contacts, fill in the blanks..")

    class Meta:
        model = AddressBook
        fields = ['first_name', 'last_name', 'address', 'phone', 'email', 'birthday']

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        # ЕЩЕ ЧЕТА ПРИДУМАТЬ
        if not phone_number.isdigit():
            raise ValidationError("Phone number should contain only digits.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        # ЕЩЕ ЧЕТА ПРИДУМАТЬ
        if not email.endswith('@example.com'):
            raise ValidationError("Invalid email address.")
        return email


class SearchContactForm(forms.Form):
    search_term = forms.CharField(max_length=100, help_text="Enter a phone number or email.")


class DeleteContactForm(forms.Form):
    contact_id = forms.IntegerField(widget=forms.HiddenInput())