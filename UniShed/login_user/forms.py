from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo
from phonenumber_field.formfields import PhoneNumberField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    phone = PhoneNumberField()

    class Meta():
        model = UserProfileInfo
        fields = ('middle_name', 'birth_date', 'phone')

