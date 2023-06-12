from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'phone_number', 'member_type', 'nation', 'email']
        widgets = {'member_type' : forms.RadioSelect}