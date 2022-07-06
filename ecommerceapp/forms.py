from tkinter import Widget
from django import forms
from .models import Order,Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =["ordered_by", "shipping_address",
                  "mobile", "email"]

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model=Customer
        fields =['username', 'password',  'full_name','email', 'address']
    
    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError('Username Already exists')
        return uname
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email alredy in use')
        return email

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class CustomerRegistrationForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput())
    address = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = User
        fields = ['username',  'full_name','email', 'address']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email alredy in use')
        return email
    
    
