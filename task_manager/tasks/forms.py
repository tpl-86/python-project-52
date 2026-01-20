from django import forms
from .models import Task
from django.contrib.auth.models import User


class CustomExecutorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.username


class TaskForm(forms.ModelForm):
    executor = CustomExecutorChoiceField(
        queryset=User.objects.all().order_by('username'),
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'id_executor'}),
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'labels',
            ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'id_name'}
                ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'id': 'id_description'}
                ),
            'status': forms.Select(
                attrs={'class': 'form-control', 'id': 'id_status'}
                ),
            'labels': forms.SelectMultiple(
                attrs={'class': 'form-control', 'id': 'id_labels'}
                ),
        }