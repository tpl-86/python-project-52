import django_filters
from .models import Task
from statuses.models import Status
from labels.models import Label
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _

class CustomExecutorFilter(django_filters.ModelChoiceFilter):
    def label_from_instance(self, obj):
        full_name = obj.get_full_name()
        return full_name if full_name else obj.username

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Статус"),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_status'}),
    )
    executor = django_filters.ChoiceFilter(
    label=_("Исполнитель"),
    choices=lambda: [(u.id, u.get_full_name() or u.username) for u in User.objects.all().order_by('first_name', 'last_name', 'username')],
    widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_executor'}),
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Метка"),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_labels'}),
    )
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label=_("Только свои задачи"),
        widget=forms.CheckboxInput(attrs={'id': 'self_tasks'})
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset