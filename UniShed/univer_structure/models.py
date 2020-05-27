from django.db import models
from login_user.models import UserProfileInfo
from django.utils.translation import gettext_lazy as _


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


class Week(models.Model):

    class WeekOfStudy(models.TextChoices):
        ODD_WEEK = 'Нечетная н.', _('Нч. неделя')
        EVEN_WEEK = 'Четная н.', _('Чт. неделя')

    week_of_study = models.CharField(max_length=20,
                                     choices=WeekOfStudy.choices,
                                     default=WeekOfStudy.ODD_WEEK
                                     )


class DayStudy(models.Model):
    class DayOfStudy(models.TextChoices):
        MONDAY = 'Понедельник', _('Пн')
        TUESDAY = 'Вторник', _('Вт')
        WEDNESDAY = 'Среда', _('Ср')
        THURSDAY = 'Четверг', _('Чт')
        FRIDAY = 'Пятница', _('Пт')
        SATURDAY = 'Суббота', _('Сб')

    week_names = models.CharField(max_length=20,
                                     choices=DayOfStudy.choices,
                                     default=DayOfStudy.ODD_WEEK
                                     )
    days_of_week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='studydays')


class Shift(models.Model):

    class ShiftOfStudy(models.TextChoices):
        FIRST_SHIFT = '1 смена', _('Первая смена')
        SECOND_SHIFT = '2 смена', _('Вторая смена')
        EVENING_SHIFT = 'Вч. смена', _('Вечерняя смена')

    name_of_shift = models.CharField(max_length=20,
                                     choices=ShiftOfStudy.choices,
                                     default=ShiftOfStudy.FIRST_SHIFT
                                      )


class Times(models.Model):

    class TimesOfStudy(models.TextChoices):
        FIRST_CLASS_TIME = '8:00-9:30', _('1.ПАРА 8:00-9:30')
        SECOND_CLASS_TIME = '9:40-11:10', _('2.ПАРА 9:40-11:10')
        THIRD_CLASS_TIME = '11:20-12:50', _('3.ПАРА 11:20-12:50')
        FOURTH_CLASS_TIME = '13:00-14:30', _('4.ПАРА 13:00-14:30')
        FIFTH_CLASS_TIME = '14:40-16:10', _('5.ПАРА 14:40-16:10')
        SIXTH_CLASS_TIME = '16:20-17:50', _('6.ПАРА 16:20-17:50')
        SEVENTH_CLASS_TIME = '18:00-19:30', _('7.ПАРА 18:00-19:30')
        EIGHTH_CLASS_TIME = '19:40-21:10', _('8.ПАРА 19:40-21:10')

    times_of_study = models.CharField(max_length=30,
                                      choices=TimesOfStudy.choices )
    shift_of_times = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name="Times")


# Specific models about students

class Degree(models.Model):

    class DegreesOfStudent(models.TextChoices):
        BACHELOR_DEGREE = 'Бакалавриат', _('Бакалавриат')
        SPECIALIST_DEGREE = 'Специалитет', _('Специалитет')
        MASTERS_DEGREE = 'Магистратура', _('Магистратура')
        PHD_DEGREE = 'Аспирантура', _('Аспирантура')

    name_degree = models.CharField(max_length=10,
                                     choices=DegreesOfStudent.choices,
                                     default=DegreesOfStudent.FIRST_COURSE)


class CourseNumber(models.Model):

    class CoursesOfStudent(models.TextChoices):
        UNDER_COURSE = '0 курс', _('Подготовительный курс')
        FIRST_COURSE = '1 курс', _('Первый курс')
        SECOND_COURSE = '2 курс', _('Второй курс')
        THIRD_COURSE = '3 курс', _('Третий курс')
        FOURTH_COURSE = '4 курс', _('Четвертый курс')
        FIFTH_COURSE = '5 курс', _('Пятый курс')

    course_numbers = models.CharField(max_length=10, choices=CoursesOfStudent.choices,
                                      default=CoursesOfStudent.FIRST_COURSE )

    program_degree = models.ForeignKey(Degree, on_delete=models.CASCADE, related_name="coursenumbers")