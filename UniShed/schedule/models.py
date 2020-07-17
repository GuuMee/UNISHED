from django.db import models
from django.utils.translation import gettext_lazy as _


class DisciplineLessons (models.Model):

    class Meta:
        verbose_name_plural = _('Занятия по дисциплинам')

    group = models.ForeignKey("univer_structure.Group", on_delete=models.CASCADE,
                              related_name="lessongroup", null=True, verbose_name='Группа')
    discipline = models.ForeignKey("univer_structure.Discipline", on_delete=models.CASCADE,
                                   related_name="disciplinelessons", null=True, verbose_name='Дисциплина')
    lector = models.ForeignKey("univer_structure.Lector", on_delete=models.CASCADE,
                               related_name="lessonlectors", null=True, verbose_name='Преподаватель')
    lecture = models.PositiveSmallIntegerField('Количество часов лекционных занятий', blank=True, null=True)
    practice = models.PositiveSmallIntegerField('Количество часов практических занятий', blank=True, null=True)
    laboratory = models.PositiveSmallIntegerField('Количество часов лабораторных занятий', blank=True, null=True)

    def __str__(self):
        return "{}".format(self.discipline)



class Times(models.Model):

    class Meta:
        verbose_name_plural = _('Временные промежутки')

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

    class Meta:
        verbose_name_plural = _('Элементы Расписания Занятий')

    class TypesOfClass(models.TextChoices):
        LECTURE = 'lecture', _('Лекционное. занятие')
        PRACTICE = 'practice', _('Практическое. занятие.')
        LABORATORY = 'laboratory', _('Лабораторное. занятие.')

    time = models.ForeignKey(Times, on_delete=models.PROTECT, related_name='schedule_items', verbose_name="Время")
    auditorium = models.ForeignKey("univer_structure.Auditorium", on_delete=models.CASCADE,
                                    related_name='course_auditorium', verbose_name="Аудитория")
    group = models.ForeignKey("univer_structure.Group", on_delete=models.CASCADE, related_name='course_students',
                                                        verbose_name="Группа")
    class_type = models.CharField(max_length=10, choices=TypesOfClass.choices, default=TypesOfClass.LECTURE,
                                                verbose_name="Тип занятия")
    lector = models.ForeignKey("univer_structure.Lector", on_delete=models.CASCADE,
                                                          related_name='course_lector', verbose_name="Преподаватель")
    discipline = models.ForeignKey("univer_structure.Discipline", on_delete=models.CASCADE,
                                                          related_name='course_discipline', verbose_name="Дисциплина")

    def __str__(self):
        return '{}  {}  {} {}  {}.'.format(self.group.name, self.auditorium.name, self.class_type,
                                         self.discipline.name, self.lector.profile.user.last_name)

