from django.db import models
from login_user.models import UserProfileInfo
from django.utils.translation import gettext_lazy as _


# Building section of the University

class Corpus(models.Model):
    name = models.CharField(max_length=5)


class Auditorium(models.Model):
    name = models.CharField(max_length=5)
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, related_name='auditoriums')


class AuditoriumType(models.Model):

    class TypesOfAuditoriums (models.TextChoices):
        LECTURE_AUDITORUIMS = 'Лекц. а.', _('Лекц. ауд.')
        PRACTICE_AUDITORUIMS = 'Практ. а.', _('Практик. ауд.')
        LABORATORIUMS = 'Лаб. а.', _('Лаб. ауд.')
        DEPARTMENT_AUDITORIUMS = 'Каф. а.', _('Аудитория кафедры')

    type_of_auditorium = models.CharField(max_length=10,
                                     choices=TypesOfAuditoriums.choices,
                                     default=TypesOfAuditoriums.LECTURE_AUDITORUIMS)


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
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='specialties')


# Users of the UniShed System

class Student(models.Model):
    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')

    class FormOfStudy(models.TextChoices):
        FULLTIME = 'ОЧ', _('Очная')
        DISTANCE = 'ЗЧ', _('Заочная')

    form_of_study = models.CharField(max_length=10,
                                     choices=FormOfStudy.choices,
                                     default=FormOfStudy.FULLTIME )


class Lector(models.Model):
    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='lectors')


class StaffDepartment(models.Model):
    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_staffs')


class StaffOther(models.Model):
    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)


# University studies

class Discipline(models.Model):
    name = models.CharField(max_length=200)
    lectors = models.ManyToManyField(Lector)


class DisciplineType(models.Model):

    class TypesOfDiscipline (models.TextChoices):
        LECTURE = 'Лк. зн.', _('Лекционное. занятие')
        PRACTICE = 'Пр. зн.', _('Практическое. занятие.')
        LABORATORY = 'Лаб. зн.', _('Лабораторное. занятие.')

    name_degree = models.CharField(max_length=10,
                                     choices=TypesOfDiscipline.choices,
                                     default=TypesOfDiscipline.LECTURE)


# Specific models about students

class Degree(models.Model):

    class DegreesOfStudent(models.TextChoices):
        BACHELOR_DEGREE = 'Бакалавриат', _('Бакалавриат')
        SPECIALIST_DEGREE = 'Специалитет', _('Специалитет')
        MASTERS_DEGREE = 'Магистратура', _('Магистратура')
        PHD_DEGREE = 'Аспирантура', _('Аспирантура')

    name_degree = models.CharField(max_length=30,
                                     choices=DegreesOfStudent.choices,
                                     default=DegreesOfStudent.BACHELOR_DEGREE)


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