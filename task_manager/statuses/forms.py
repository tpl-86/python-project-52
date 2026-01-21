from django import forms

from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "name": {
                "unique": "Task status с таким Имя уже существует.",
            },
        }
