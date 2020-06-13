from django.db import models
from django.utils.translation import gettext_lazy as _

'''
class LectorAttachedDiscipline(models.Model):

    class Meta:
        verbose_name_plural = _('Преподаватели и их дисциплины')
        unique_together = (('lector', 'discipline'))

    lector = models.ForeignKey("univer_structure.Lector", on_delete=models.CASCADE, related_name="attached_lectors")
    discipline = models.ForeignKey("univer_structure.Discipline", on_delete=models.CASCADE, related_name="attached_discipline")

    def __str__(self):
        return "{} - {}".format(self.lector, self.discipline)
'''


class DisciplineLessons (models.Model):

    class Meta:
        verbose_name_plural = _('Занятия по дисциплинам')

    group = models.ForeignKey("univer_structure.Group", on_delete=models.CASCADE,
                              related_name="lessongroup", null=True)
    discipline = models.ForeignKey("univer_structure.Discipline", on_delete=models.CASCADE,
                                   related_name="disciplinelessons", null=True)
    lector = models.ForeignKey("univer_structure.Lector", on_delete=models.CASCADE,
                               related_name="lessonlectors", null=True)
    lecture = models.PositiveSmallIntegerField(blank=True, null=True)
    practice = models.PositiveSmallIntegerField(blank=True, null=True)
    laboratory = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.discipline)


class Shift(models.Model):

    class ShiftOfStudy(models.TextChoices):
        FIRST_SHIFT = '1 смена', _('Первая смена')
        SECOND_SHIFT = '2 смена', _('Вторая смена')
        EVENING_SHIFT = 'Вч. смена', _('Вечерняя смена')

    name_of_shift = models.CharField(max_length=20, choices=ShiftOfStudy.choices,
                                     default=ShiftOfStudy.FIRST_SHIFT)


class CourseStudent(models.Model):

    class WeekOfStudy(models.TextChoices):
        ODD_WEEK = 'Нечетная н.', _('Нч. неделя')
        EVEN_WEEK = 'Четная н.', _('Чт. неделя')

    week_of_study = models.CharField(max_length=20, choices=WeekOfStudy.choices, default=WeekOfStudy.ODD_WEEK)


class Times(models.Model):

    class DayOfStudy(models.TextChoices):
        MONDAY = 'Понедельник', _('Пн')
        TUESDAY = 'Вторник', _('Вт')
        WEDNESDAY = 'Среда', _('Ср')
        THURSDAY = 'Четверг', _('Чт')
        FRIDAY = 'Пятница', _('Пт')
        SATURDAY = 'Суббота', _('Сб')

    class WeekOfStudy(models.TextChoices):
        ODD_WEEK = 'Нечетная н.', _('Нч. неделя')
        EVEN_WEEK = 'Четная н.', _('Чт. неделя')

    class TimesOfStudy(models.TextChoices):
        FIRST_CLASS_TIME = '8:00-9:30', _('1.ПАРА 8:00-9:30')
        SECOND_CLASS_TIME = '9:40-11:10', _('2.ПАРА 9:40-11:10')
        THIRD_CLASS_TIME = '11:20-12:50', _('3.ПАРА 11:20-12:50')
        FOURTH_CLASS_TIME = '13:00-14:30', _('4.ПАРА 13:00-14:30')
        FIFTH_CLASS_TIME = '14:40-16:10', _('5.ПАРА 14:40-16:10')
        SIXTH_CLASS_TIME = '16:20-17:50', _('6.ПАРА 16:20-17:50')
        SEVENTH_CLASS_TIME = '18:00-19:30', _('7.ПАРА 18:00-19:30')
        EIGHTH_CLASS_TIME = '19:40-21:10', _('8.ПАРА 19:40-21:10')

    time = models.CharField(max_length=30, choices=TimesOfStudy.choices)
    day = models.CharField(max_length=30, choices=DayOfStudy.choices)
    week_type = models.CharField(max_length=30, choices=WeekOfStudy.choices)

    def __str__(self):
        return '{}: {}, {}'.format(self.day, self.time, self.week_type)


class CourseScheduleItem(models.Model):

    class DayOfStudy(models.TextChoices):
        MONDAY = 'Понедельник', _('Пн')
        TUESDAY = 'Вторник', _('Вт')
        WEDNESDAY = 'Среда', _('Ср')
        THURSDAY = 'Четверг', _('Чт')
        FRIDAY = 'Пятница', _('Пт')
        SATURDAY = 'Суббота', _('Сб')

    class IntensityOfCourse(models.TextChoices):
        ONCE_A_WEEK = '1 раз в неделю', _('1р. в нед.')
        BETWEEN_WEEKS = 'Через неделю', _('1р. в 2 нед.')

    class TypesOfClass(models.TextChoices):
        LECTURE = 'lecture', _('Лекционное. занятие')
        PRACTICE = 'practice', _('Практическое. занятие.')
        LABORATORY = 'laboratory', _('Лабораторное. занятие.')

    class_type = models.CharField(max_length=10, choices=TypesOfClass.choices, default=TypesOfClass.LECTURE)
    time = models.ForeignKey(Times, on_delete=models.PROTECT, related_name='schedule_items')
    auditorium = models.ForeignKey("univer_structure.Auditorium", on_delete=models.CASCADE,
                                             related_name='course_auditorium')
    lector = models.ForeignKey("univer_structure.Lector", on_delete=models.CASCADE,
                                         related_name='course_lector')
    discipline = models.ForeignKey("univer_structure.Discipline", on_delete=models.CASCADE,
                                             related_name='course_discipline')
    group = models.ForeignKey("univer_structure.Group", on_delete=models.CASCADE, related_name='course_students')
    potok = models.BooleanField(default=False)
    half_group = models.BooleanField(default=True)
    quantity_z = models.PositiveIntegerField(default=18)
    intensity = models.CharField(max_length=15, choices=IntensityOfCourse.choices,
                                 default=IntensityOfCourse.BETWEEN_WEEKS)  # 1 time a week/1 time in 2 weeks


