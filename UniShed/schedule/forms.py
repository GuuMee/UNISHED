from django.forms import ModelForm

from schedule.models import CourseScheduleItem


class CourseScheduleItemForm(ModelForm):
    class Meta:
        model = CourseScheduleItem
        exclude = (
        )