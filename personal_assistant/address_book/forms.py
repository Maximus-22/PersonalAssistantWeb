from datetime import datetime
import re

from dateutil import parser
from django import forms
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date

from .models import AddressBook


class AddressBookForm(forms.ModelForm):
    first_name = forms.CharField(min_length=3, max_length=32, widget=forms.TextInput(attrs={'style': 'width: 30%;'}))
    last_name = forms.CharField(min_length=3, max_length=32, widget=forms.TextInput(attrs={'style': 'width: 30%;'}))
    address = forms.CharField(min_length=5, max_length=255, widget=forms.TextInput(attrs={'style': 'width: 50%;'}))
    phone = forms.CharField(min_length=13, max_length=16, widget=forms.TextInput(attrs={'style': 'width: 30%;'}))
    email = forms.EmailField(min_length=10, max_length=254, widget=forms.TextInput(attrs={'style': 'width: 30%;'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = AddressBook
        fields = ['first_name', 'last_name', 'address', 'phone', 'email', 'birthday']

    def __init__(self, *args, **kwargs):
        super(AddressBookForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Iм'я"
        self.fields['last_name'].label = 'Прізвище'
        self.fields['address'].label = 'Адреса проживання'
        self.fields['phone'].label = 'Телефон'
        self.fields['email'].label = 'Електронна адреса'
        self.fields['birthday'].label = 'День народження'
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.birthday:
                self.initial['birthday'] = instance.birthday.strftime('%Y-%m-%d')

    def clean_name(self):
        first_name = self.cleaned_data['first_name']
        cleaned_first_name = r'^[A-Za-zА-Яа-яІіЄєЇї]+$'
        if not re.match(cleaned_first_name, first_name):
            raise ValidationError("Ім'я має містити лише літери без пробілів.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        cleaned_last_name = r'^[A-Za-zА-Яа-яІіЄєЇї]+$'
        if not re.match(cleaned_last_name, last_name):
            raise ValidationError("Прізвище має містити лише літери без пробілів.")
        return last_name

    def clean_address(self):
        address = self.cleaned_data['address']
        if not address:
            raise forms.ValidationError("Адреса не може бути порожньою.")
        if not re.match(r'^[\w\s,.\-#]*$', address):
            raise forms.ValidationError("Адреса містить неприпустимі символи.")
        return address

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        cleaned_number = re.sub(r'[^+0-9]', '', phone_number)
        return cleaned_number


class SearchContactForm(forms.Form):
    query = forms.CharField(min_length=3, max_length=32, required=False, initial='')


class DeleteContactForm(forms.Form):
    confirm_delete = forms.BooleanField(required=True, initial=False, widget=forms.HiddenInput, )


class BirthdayContactForm(forms.Form):
    shift_day = forms.IntegerField(min_value=0, max_value=364, required=False)
