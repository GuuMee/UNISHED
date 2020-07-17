from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class UserProfileInfo(models.Model): #this class inherit from models.Model
    class Meta:
        verbose_name_plural = _('Информация о пользователях UNISHED')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile") #that's extending the class oneToOne -relationship, field with the user itself
    #the reason for that is because this is a Model class to add an additional information that the defaultuser doesn't have

    #additional
    middle_name = models.CharField(max_length=30, verbose_name=_("Отчество"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Дата рождения"))
    phone = PhoneNumberField(null=True, blank=True, unique=True, verbose_name=_("Телефон"))

    def __str__(self):
        return self.user.last_name

    def get_user_type(self):
        if hasattr(self, 'student'):
            return 'student'
        elif hasattr(self, 'lector'):
            return 'lector'
