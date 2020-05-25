import datetime
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from .models import UserProfileInfo
from phonenumber_field.formfields import PhoneNumberField
from bootstrap_datepicker_plus import DatePickerInput
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label=_("Пароль"))
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label=_("Повторить  пароль"))

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )

class UserProfileInfoForm(forms.ModelForm):
    phone = PhoneNumberField(label=_("Телефон"))
    birth_date = forms.DateField(
        widget=DatePickerInput(
            options={'locale': settings.LANGUAGE_CODE,
                     'minDate': str(datetime.date.today() - datetime.timedelta(days=settings.MIN_BIRTH_DATE)),
                     'maxDate': str(datetime.date.today() - datetime.timedelta(days=settings.MAX_BIRTH_DATE)),
                     },
            format=settings.DATE_INPUT_FORMATS,
        ),
        label=_("Дата рождения")
    )

    class Meta():
        model = UserProfileInfo
        fields = ('middle_name', 'birth_date', 'phone')

