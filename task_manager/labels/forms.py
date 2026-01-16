from django import forms
from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_name'}),
        }
        error_messages = {
            'name': {'unique': "Метка с таким именем уже существует."},
        }