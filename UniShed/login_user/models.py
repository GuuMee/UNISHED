from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
# Create your models here.

# University entities


class Institute(models.Model):
    name = models.CharField(max_length=50, blank=False)


class Faculty(models.Model):
    name = models.CharField(max_length=50)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='faculties')


class Department(models.Model):
    name = models.CharField(max_length=30)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')


class Group(models.Model):
    name = models.CharField(max_length=10)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='groups')



#USERS

class UserProfileInfo(models.Model): #this class inherit from models.Model

    user = models.OneToOneField(User, on_delete=models.CASCADE) #that's extending the class oneToOne -relationship, field with the user itself
    #the reason for that is because this is a Model class to add an additional information that the defaultuser doesn't have

    #additional
    middle_name = models.CharField(max_length=30, verbose_name=_("Отчество"))
    birth_date = models.DateField(null=False, blank=False, verbose_name=_("Дата рождения"))
    phone = PhoneNumberField(null=False, blank=False, unique=True, verbose_name=_("Телефон"))

    def __str__(self):
        return self.user.username


class Student(models.Model):

    class FormOfStudy(models.TextChoices):
        FULLTIME = 'ОЧ', _('Очная')
        DISTANCE = 'ЗЧ', _('Заочная')

    student_profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)


    #fields for students
    student_card_n = models.CharField(max_length=7, blank=False, null=False)
    form_of_study = models.CharField(max_length=2,
                                     choices=FormOfStudy.choices,
                                     default=FormOfStudy.FULLTIME )

    def is_upperclass(self):
        return self.form_of_study in {self.FormOfStudy.FULLTIME, self.FormOfStudy.DISTANCE,}

    group_n = models.TextField(max_length=6, blank=False)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='students')


class Lector(models.Model):
    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='lectors')

class Staff(models.Model):
    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
