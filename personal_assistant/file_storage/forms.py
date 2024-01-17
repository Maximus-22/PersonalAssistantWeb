from django import forms
from django.core.exceptions import ValidationError


class FileUploadForm(forms.Form):
    file = forms.FileField()
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), required=False)

    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = 'Файл'
        self.fields['description'].label = 'Опис, змiст'

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            max_size = 2 * 1024 * 1024
            if file.size > max_size:
                raise ValidationError('Розмір файлу не повинен перевищувати 2 МБ.')
        return file
