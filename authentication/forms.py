from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)
        widgets = {
            "username": forms.TextInput(attrs={"class": "form_control"}),
            "password": forms.PasswordInput(
                attrs={"class": "form_control", "data-toggle": "password"}
            ),
        }
