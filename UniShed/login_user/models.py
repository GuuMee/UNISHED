from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumber
from django.utils.translation import gettext_lazy as _
# Create your models here.

class UserProfileInfo(models.Model): #this class inherit from models.Model

    user = models.OneToOneField(User) #that's extending the class oneToOne -relationship, field with the user itself
    #the reason for that is because this is a Model class to add an additional information that the defaultuser doesn't have

    #additional
    middle_name = models.TextField(max_length=30)
    birth_date = models.DateField(null=False, blank=False)
    phone = PhoneNumber.from_string(phone_number=raw_phone, region='RU').as_e164
    #specialization =
    #department =

    def __str__(self):
        return self.user.username

class Student(models.Model):

    #fields for students
    student_card_num = models.CharField(max_length=7, blank=False, null=False)

    class FormOfStudy(models.TextChoices):
        FULLTIME = 'ОЧ', _('Очная')
        DISTANCE = 'ЗЧ', _('Заочная')

        form_of_study = models.CharField(
            max_lengh = 2,
            choices = FormOfStudy.choices,
            default = FormOfStudy.FULLTIME )

        def is_upperclass(self):
            return self.form_of_study in {
                self.FormOfStudy.FULLTIME,
                self.FormOfStudy.DISTANCE,
            }


    #faculty =
    #group_n =
