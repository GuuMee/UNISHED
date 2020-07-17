from django.db import models
from login_user.models import UserProfileInfo
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _


# Таблица Занятие (Discipline, Lector, Group) определяет какие именно занятия по каким дисциплинам и в каких группах
# должен провести определенный определенный преподаватель

# Building section of the University

class Corpus(models.Model):

    class Meta:
        verbose_name_plural = _('Корпуса')

    name = models.CharField(max_length=100, verbose_name='Название корпуса')

    def __str__(self):
        return self.name


# Hierarchy of the University

class Institute(models.Model):

    class Meta:
        verbose_name_plural = _('Интситуты')

    name = models.CharField(max_length=200, blank=False, verbose_name='Название института')

    def __str__(self):
        return self.name


class Faculty(models.Model):

    class Meta:
        verbose_name_plural = _('Факультеты')

    name = models.CharField(max_length=200, verbose_name='Название факультета')
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='faculties',
                                  verbose_name='Институт')

    def __str__(self):
        return self.name


class Department(models.Model):

    class Meta:
        verbose_name_plural = _('Кафедры')

    name = models.CharField(max_length=200, verbose_name='Название кафедры')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments',
                                verbose_name='Факультет')
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, related_name='corpus_departments',
                               verbose_name='Корпус', null=True, blank=True)

    def __str__(self):
        return self.name


class Auditorium(models.Model):

    class Meta:
        verbose_name_plural = _('Аудитории')

    class TypesOfAuditoriums (models.TextChoices):
        AUDITORIUM = 'Аудитория', _('Аудитория')
        STUDY_LABORATORIUMS = 'Уч. Лаб.', _('Учебная Лабораторная')
        STUDY_AUD = 'Уч. класс', _('Учебный класс')
        COMP_AUD = 'Комп. класс', _('Компьютерные класс')
        DEPARTMENT_AUDITORIUMS = 'Каф. а.', _('Аудитория кафедры')


    class TypesOfDiscipline(models.TextChoices):
        LECTURE = 'Лк. зн.', _('Лекции')
        PRACTICE = 'Пр. зн.', _('Практика')
        LABORATORY = 'Лаб. зн.', _('Лабораторные работы')

    name = models.CharField(max_length=50, verbose_name='Название')
    type_of_auditorium = models.CharField(max_length=30, choices=TypesOfAuditoriums.choices,
                                          default=TypesOfAuditoriums.AUDITORIUM,
                                          verbose_name='Тип аудитории')

    type_discipline = MultiSelectField( choices=TypesOfDiscipline.choices,
                                       null=True, verbose_name="Вид учебных занятий")
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, related_name='corpusauditoriums', verbose_name='Корпус')
    capacity = models.PositiveIntegerField(default=25, verbose_name='Вмеестимость')
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='dept_aucitoriums', verbose_name='Кафедра',
                                        default=62)


    def __str__(self):
        return self.name



class Specialty(models.Model):

    class Meta:
        verbose_name_plural = _('Специальности')

    name = models.CharField(max_length=200, verbose_name='Название специальности')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='specialties', verbose_name='Факультет')

    def __str__(self):
        return self.name


class Profile(models.Model):

    class Meta:
        verbose_name_plural = _('Профили Специальностей')

    name = models.CharField(max_length=200, verbose_name='Название профиля')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='profiles', verbose_name='Специальность')

    def __str__(self):
        return self.name

# University studies


class Discipline(models.Model):

    class Meta:
        verbose_name_plural = _('Дисциплины')


    name = models.CharField(max_length=200, unique=True)
    department = models.ForeignKey(Department, related_name="disciplines", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Group(models.Model):

    class Meta:
        verbose_name_plural = _('Группы')

    class DegreesOfStudent(models.TextChoices):
        BACHELOR_DEGREE = 'Бакалавриат', _('Бакалавриат')
        SPECIALIST_DEGREE = 'Специалитет', _('Специалитет')
        MASTERS_DEGREE = 'Магистратура', _('Магистратура')
        PHD_DEGREE = 'Аспирантура', _('Аспирантура')

    class CoursesOfStudent(models.TextChoices):
        UNDER_COURSE = '0 курс', _('Подготовительный курс')
        FIRST_COURSE = '1 курс', _('Первый курс')
        SECOND_COURSE = '2 курс', _('Второй курс')
        THIRD_COURSE = '3 курс', _('Третий курс')
        FOURTH_COURSE = '4 курс', _('Четвертый курс')
        FIFTH_COURSE = '5 курс', _('Пятый курс')

    name = models.CharField(max_length=10, verbose_name='Название группы')
    degree = models.CharField(max_length=30, choices=DegreesOfStudent.choices, default=DegreesOfStudent.BACHELOR_DEGREE,
                              verbose_name='Ступень обучения')
    course_number = models.CharField(max_length=10, choices=CoursesOfStudent.choices,
                                     default=CoursesOfStudent.FIRST_COURSE, verbose_name='Номер курса')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="groups", blank=True, null=True, verbose_name="Профиль")
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='groupspecialties',
                                  verbose_name='Специальность')
    quantity_students = models.CharField(max_length=5, null=True, verbose_name='Количество студентов')

    def __str__(self):
        return self.name


# Users of the UniShed System

class Student(models.Model):

    class Meta:
        verbose_name_plural = _('Студенты')

    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE, related_name="student")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students', verbose_name='Группа')

    class FormOfStudy(models.TextChoices):
        FULLTIME = 'ОЧ', _('Очная')
        DISTANCE = 'ЗЧ', _('Заочная')

    form_of_study = models.CharField(max_length=10, choices=FormOfStudy.choices, default=FormOfStudy.FULLTIME,
                                     verbose_name='Форма обучения')

    def __str__(self):
        return self.profile.user.last_name


class Lector(models.Model):

    class Meta:
        verbose_name_plural = _('Преподаватели')

    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE, related_name="lector")
    department = models.ManyToManyField(Department, related_name="lectordepartments")
    # don't delete disciplines field below because it contains connected disciplines to the lector
    disciplines = models.ManyToManyField(Discipline, related_name="lectordisciplines")

    def __str__(self):
        return "{} {} {}".format(self.profile.user.last_name, self.profile.user.first_name, self.profile.middle_name)


class StaffDepartment(models.Model):

    class Meta:
        verbose_name_plural = _('Сотрудники кафедр')

    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_staffs')

    def __str__(self):
        return self.profile.user.last_name

class StaffOther(models.Model):

    class Meta:
        verbose_name_plural = _('Другие сотрудники')

    profile = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.last_name








