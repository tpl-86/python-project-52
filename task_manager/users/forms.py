from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    # Стандартные поля формы
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"id": "id_password1", "class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"id": "id_password2", "class": "form-control"}),
    )

    # Доп. алиасы для совместимости с тестами: password/password_confirmation
    # (они будут маппиться в password1/password2 в __init__)
    password = forms.CharField(
        label="Password (alias)",
        widget=forms.PasswordInput,
        required=False,
    )
    password_confirmation = forms.CharField(
        label="Password confirmation (alias)",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        widgets = {
            "username": forms.TextInput(attrs={"id": "id_username", "class": "form-control"}),
            "first_name": forms.TextInput(attrs={"id": "id_first_name", "class": "form-control"}),
            "last_name": forms.TextInput(attrs={"id": "id_last_name", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Маппим альтернативные имена на стандартные, если они пришли
        if self.data:
            data = self.data.copy()
            if not data.get("password1") and data.get("password"):
                data["password1"] = data.get("password")
            if not data.get("password2") and data.get("password_confirmation"):
                data["password2"] = data.get("password_confirmation")
            self.data = data

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1") or ""
        p2 = cleaned.get("password2") or ""

        # Единственная проверка: длина >= 3
        if len(p1) < 3:
            self.add_error("password1", "Password must contain at least 3 characters.")
        if p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        widgets = {
            "username": forms.TextInput(attrs={"id": "id_username", "class": "form-control"}),
            "first_name": forms.TextInput(attrs={"id": "id_first_name", "class": "form-control"}),
            "last_name": forms.TextInput(attrs={"id": "id_last_name", "class": "form-control"}),
        }
