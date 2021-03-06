from django.db import models
from django.utils.translation import gettext_lazy as _


class LectorAttachedDiscipline(models.Model):
    lector = models.ForeignKey("univer_structure.Lector", on_delete=models.CASCADE)
    discipline = models.ForeignKey("univer_structure.Discipline", on_delete=models.CASCADE)


class CourseStudent(models.Model):
    group_number = models.ForeignKey("univer_structure.Group", on_delete=models.CASCADE, related_name="students_in_gr")


class CourseScheduleItem(models.Model):

    class TimesOfStudy(models.TextChoices):
        FIRST_CLASS_TIME = '8:00-9:30', _('1.ПАРА 8:00-9:30')
        SECOND_CLASS_TIME = '9:40-11:10', _('2.ПАРА 9:40-11:10')
        THIRD_CLASS_TIME = '11:20-12:50', _('3.ПАРА 11:20-12:50')
        FOURTH_CLASS_TIME = '13:00-14:30', _('4.ПАРА 13:00-14:30')
        FIFTH_CLASS_TIME = '14:40-16:10', _('5.ПАРА 14:40-16:10')
        SIXTH_CLASS_TIME = '16:20-17:50', _('6.ПАРА 16:20-17:50')
        SEVENTH_CLASS_TIME = '18:00-19:30', _('7.ПАРА 18:00-19:30')
        EIGHTH_CLASS_TIME = '19:40-21:10', _('8.ПАРА 19:40-21:10')

    class DayOfStudy(models.TextChoices):
        MONDAY = 'Понедельник', _('Пн')
        TUESDAY = 'Вторник', _('Вт')
        WEDNESDAY = 'Среда', _('Ср')
        THURSDAY = 'Четверг', _('Чт')
        FRIDAY = 'Пятница', _('Пт')
        SATURDAY = 'Суббота', _('Сб')

    class ShiftOfStudy(models.TextChoices):
        FIRST_SHIFT = '1 смена', _('Первая смена')
        SECOND_SHIFT = '2 смена', _('Вторая смена')
        EVENING_SHIFT = 'Вч. смена', _('Вечерняя смена')

    class WeekOfStudy(models.TextChoices):
        ODD_WEEK = 'Нечетная н.', _('Нч. неделя')
        EVEN_WEEK = 'Четная н.', _('Чт. неделя')

    week_of_study = models.CharField(max_length=20, choices=WeekOfStudy.choices, default=WeekOfStudy.ODD_WEEK)
    name_of_shift = models.CharField(max_length=20, choices=ShiftOfStudy.choices,
                                     default=ShiftOfStudy.FIRST_SHIFT)
    day = models.CharField(max_length=20, choices=DayOfStudy.choices)
    times_of_study = models.CharField(max_length=30, choices=TimesOfStudy.choices)
    auditorium = models.ForeignKey("univer_structure.Auditorium", on_delete=models.CASCADE,
                                             related_name='course_auditorium')
    lector = models.ForeignKey("univer_structure.Lector", on_delete=models.CASCADE,
                                         related_name='course_lector')
    discipline = models.ForeignKey("univer_structure.Discipline", on_delete=models.CASCADE,
                                             related_name='course_discipline')
    group = models.ForeignKey(CourseStudent, on_delete=models.CASCADE, related_name='course_students')

