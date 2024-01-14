from django import forms
from .models import Notebook, Tag



class NotebookForm(forms.ModelForm):
    tags = forms.CharField(max_length=84, help_text="Введіть теги через кому.")

    class Meta:
        model = Notebook
        fields = ['title', 'description', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        return [tag.strip() for tag in tags.split(',')]
    

class DeleteNoteForm(forms.Form):
    confirm_delete = forms.BooleanField(required=True, initial=False, widget=forms.HiddenInput,)


class SearchNoteForm(forms.Form):
    query = forms.CharField(min_length=3, max_length=32, required=False, initial='')
