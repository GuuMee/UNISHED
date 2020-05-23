from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label=_("Пароль"))

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    phone = PhoneNumberField(label=_("Телефон"))
    birth_date = forms.DateField(widget=AdminDateWidget(), label=_("Дата рождения"))

    class Meta():
        model = UserProfileInfo
        fields = ('middle_name', 'birth_date', 'phone')

