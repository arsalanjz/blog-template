from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class UserRegisterForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        if  User.objects.filter(email=email).exists():
            raise ValidationError('Email already exits')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('username already exits')
        return username




class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())