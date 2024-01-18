from django import forms
from django.core.exceptions import ValidationError

from .models import AddressBook

import re


class AddressBookForm(forms.ModelForm):
    birthday = forms.CharField(max_length=10)
    class Meta:
        model = AddressBook
        fields = ['first_name', 'last_name', 'address', 'phone', 'email', 'birthday']

    def clean_name(self):
        first_name = self.cleaned_data['first_name']

        cleaned_first_name = r'^[A-Za-zА-Яа-я]+$'

        if not re.match(cleaned_first_name, first_name):
            raise ValidationError("Ім'я має містити лише літери без пробілів.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        cleaned_last_name = r'^[A-Za-zА-Яа-я]+$'

        if not re.match(cleaned_last_name, last_name):
            raise ValidationError("Прізвище має містити лише літери без пробілів.")

        return last_name


    def clean_address(self):
        address = self.cleaned_data['address']

        cleaned_address = r'^[A-Za-zА-Яа-я]+$'

        if not re.match(cleaned_address, address):
            raise ValidationError("Прізвище має містити лише літери без пробілів.")

        return address


    def clean_phone(self):
        phone_number = self.cleaned_data['phone']

        cleaned_number = re.sub(r'\D', '', phone_number)

        # Проверка, что осталось от 8 до 12 цифр
        if not (8 <= len(cleaned_number) <= 12):
            raise ValidationError("Номер телефону має містити від 8 до 12 цифр.")

        return cleaned_number

    def clean_email(self):
        email = self.cleaned_data['email']

        # Проверка формата имейла с использованием регулярного выражения
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email address format.")

        return email


    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']

        pattern = re.compile(r'^\d{2}\.\d{2}.\d{4}$')
        if not pattern.match(birthday):
            raise forms.ValidationError('Invalid date format. Use the format DD.MM.YYYY.')

        return birthday




class SearchContactForm(forms.Form):
    query = forms.CharField(min_length=3, max_length=32, required=False, initial='')


class DeleteContactForm(forms.Form):
    contact_id = forms.IntegerField(widget=forms.HiddenInput())
