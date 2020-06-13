from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from schedule.algorithm.genetic_alg import run

from schedule.models import Times, DisciplineLessons, CourseScheduleItem
# Register your models here.

admin.site.register(DisciplineLessons)
admin.site.register(Times)


@admin.register(CourseScheduleItem)
class CourseScheduleAdmin(admin.ModelAdmin):
    change_list_template = "schedule/alg.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('run/', self.run_algoritm),
        ]
        return my_urls + urls

    def run_algoritm(self, request):
        run()
        return HttpResponseRedirect("../")
