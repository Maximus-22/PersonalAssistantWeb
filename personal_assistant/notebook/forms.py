from django import forms
from .models import Notebook, Tag


class NotebookForm(forms.ModelForm):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'style': 'width: 30%;'}))
    tags = forms.CharField(max_length=84, widget=forms.TextInput(attrs={'style': 'width: 30%;'}),
                           help_text="Введіть теги через кому.")

    class Meta:
        model = Notebook
        fields = ['title', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super(NotebookForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Заголовок'
        self.fields['description'].label = 'Опис, змiст'
        self.fields['tags'].label = '#Тег, або #теги'

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        return [tag.strip() for tag in tags.split(',')]


class DeleteNoteForm(forms.Form):
    confirm_delete = forms.BooleanField(required=True, initial=False, widget=forms.HiddenInput, )


class SearchNoteForm(forms.Form):
    query = forms.CharField(min_length=3, max_length=32, required=False, initial='')

