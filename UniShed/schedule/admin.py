from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from schedule.algorithm.genetic_alg import run

from schedule.models import Times, DisciplineLessons, CourseScheduleItem
# Register your models here.

admin.site.register(DisciplineLessons)


@admin.register(CourseScheduleItem)
class CourseScheduleAdmin(admin.ModelAdmin):
    change_list_template = "schedule/alg.html"
    readonly_fields =["group", "discipline"]
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('run/', self.run_algoritm),
        ]
        return my_urls + urls

    def run_algoritm(self, request):
        run()
        return HttpResponseRedirect("../")


@admin.register(Times)
class Times(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
