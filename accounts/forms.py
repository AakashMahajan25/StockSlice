from django import forms
import string
import re
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        alphanumeric_pattern = re.compile(r'^[a-zA-Z0-9_]+$')
        if not alphanumeric_pattern.match(first_name):
            raise forms.ValidationError('First name should only contain letters and numbers')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        alphanumeric_pattern = re.compile(r'^[a-zA-Z0-9_]+$')
        if not alphanumeric_pattern.match(last_name):
            raise forms.ValidationError('Last name should only contain letters and numbers')
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        alphanumeric_pattern = re.compile(r'^[a-zA-Z0-9_]+$')
        if not alphanumeric_pattern.match(username):
            raise forms.ValidationError('Username should only contain letters and numbers')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        if len(password) < 6:
            raise forms.ValidationError('Password length should be at least 6 characters')
        if not any(char.isalpha() for char in password) or not any(char.isdigit() or char in string.punctuation for char in password):
            raise forms.ValidationError('Password should contain at least one letter and one digit or punctuation character')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already taken')
        return email

class ProfileForm(forms.Form):
    profile_image = forms.ImageField()