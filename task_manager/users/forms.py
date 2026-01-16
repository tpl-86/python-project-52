from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
    
    def _post_clean(self):
        forms.ModelForm._post_clean(self)
        pwd = self.cleaned_data.get('password2')
        if pwd:
            digits = sum(ch.isdigit() for ch in pwd)
            if digits < 3:
                msg = "Пароль должен содержать не менее 3 цифр."
                # добавим ошибку к обоим полям пароля
                self.add_error('password1', ValidationError(msg))
                self.add_error('password2', ValidationError(msg))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')