from django.db import models


class CourseStudent(models.Model):
    degree_name = models.ForeignKey("univer_structure.Degree", on_delete=models.CASCADE, related_name='degrees')
    course_number = models.ForeignKey("univer_structure.CourseNumber", on_delete=models.CASCADE, related_name="coursesnum")
    group_number = models.ForeignKey("univer_structure.Group", on_delete=models.CASCADE, related_name="groups")


class LectorAttachedDiscipline(models.Model):
    lector = models.ForeignKey("univer_structure.Lector")
    discipline = models.ForeignKey("univer_structure.Discipline")


class CourseScheduleItem(models.Model):
    auditorium_of_course = models.ForeignKey("univer_structure.Auditorium", on_delete=models.CASCADE,
                                             related_name='courseauditorium')
    lector_of_course = models.ForeignKey("univer_structure.Lector", on_delete=models.CASCADE, related_name='courselectors')
    discipline_of_course = models.ForeignKey("univer_structure.Discipline", on_delete=models.CASCADE, related_name='disciplines')
    student_course = models.ForeignKey(CourseStudent, on_delete=models.CASCADE, related_name='groups')


class WeekCourseSchedule(models.Model):
    week_of_course = models.ForeignKey("univer_structure.Week", on_delete=models.CASCADE, related_name='courseweek')
    time_of_course = models.ForeignKey("univer_structure.Times", on_delete=models.CASCADE, related_name='coursetimes')
    course_item = models.ForeignKey (CourseScheduleItem, on_delete=models.CASCADE, related_name='courses')




