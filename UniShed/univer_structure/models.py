from django.db import models
from login_user.models import UserProfileInfo
from django.utils.translation import gettext_lazy as _

# Create your models here.


# Building section of the University

class Corpus(models.Model):
    name = models.CharField(max_length=5)


class Auditorium(models.Model):
    name = models.CharField(max_length=5)
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, related_name='auditoriums')


# Hierarchy of the University

class Institute(models.Model):
    name = models.CharField(max_length=50, blank=False)


class Faculty(models.Model):
    name = models.CharField(max_length=50)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='faculties')


class Department(models.Model):
    name = models.CharField(max_length=30)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')


class Specialty(models.Model):
    name = models.CharField(max_length=50)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='specialties')


class Group(models.Model):
    name = models.CharField(max_length=10)
    specialty = models.ForeignKey(on_delete=models.CASCADE, related_name='specialties')


# Users of the UniShed System

class Student(models.Model):
    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
    group = models.ForeignKey(on_delete=models.CASCADE, related_name='students')

    class FormOfStudy(models.TextChoices):
        FULLTIME = 'ОЧ', _('Очная')
        DISTANCE = 'ЗЧ', _('Заочная')

    form_of_study = models.CharField(max_length=10,
                                     choices=FormOfStudy.choices,
                                     default=FormOfStudy.FULLTIME )

    def is_upperclass(self):
        return self.form_of_study in {self.FormOfStudy.FULLTIME, self.FormOfStudy.DISTANCE,}


class Lector(models.Model):
    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
    department = models.ForeignKey(on_delete=models.CASCADE, related_name='lectors')


class StaffDepartment(models.Model):
    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
    department = models.ForeignKey(on_delete=models.CASCADE, related_name='department_staffs')


class StaffOther(models.Model):
    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)


# University studies

class Discipline(models.Model):
    name = models.CharField(max_length='100')
    lectors = models.ManyToManyField(Lector)

class Shift(models.Model):

    class ShiftOfStudy(models.TextChoices):
        FIRST_SHIFT = '1 смена', _('Первая смена')
        SECOND_SHIFT = '2 смена', _('Вторая смена')
        EVENING_SHIFT = 'Вч. смена', _('Вечерняя смена')

    shift_of_study = models.CharField(max_length=20,
                                     choices=ShiftOfStudy.choices,
                                     default=ShiftOfStudy.FIRST_SHIFT
                                      )

    def is_upperclass(self):
        return self.shift_of_study in {self.ShiftOfStudy.FIRST_SHIFT,
                                       self.ShiftOfStudy.SECOND_SHIFT,
                                       self.ShiftOfStudy.EVENING_SHIFT
                                       }

class Week(models.Model):

    class WeekOfStudy(models.TextChoices):
        ODD_WEEK = 'Нечетная н.', _('Нч. неделя')
        EVEN_WEEK = 'Четная н.', _('Чт. неделя')

    week_of_study = models.CharField(max_length=20,
                                     choices=WeekOfStudy.choices,
                                     default=WeekOfStudy.ODD_WEEK
                                     )

    def is_upperclass(self):
        return self.week_of_study in {self.WeekOfStudy.ODD_WEEK, self.WeekOfStudy.EVEN_WEEK}
