from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

MEMBER_TYPE = (('Customer', 'Customer'), ('Counselor', 'Counselor'))
NATION = (('Korean', 'Korean'), ('English', 'English'), ('Japanese', 'Japanese'), 
          ('Chinese', 'Chinese'), ('Vietnamese', 'Vietnamese'), ('Thai', 'Thai'))

class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Check Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email Address')
    phone_number = forms.CharField(label='Phone number', max_length=11)
    member_type = forms.CharField(label='User type', widget=forms.Select(choices=MEMBER_TYPE), max_length=20)
    nation = forms.ChoiceField(label='Language', choices=NATION)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'phone_number', 'member_type', 'nation']
        widgets = {'member_type' : forms.RadioSelect}

