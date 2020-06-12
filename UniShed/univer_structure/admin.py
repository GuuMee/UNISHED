from django.contrib import admin
from univer_structure.models import Corpus, Auditorium, Institute, Faculty, Department, Lector, Discipline, Group, \
    Specialty, Profile
# Register your models here.

admin.site.register(Institute)
admin.site.register(Faculty)
admin.site.register(Specialty)
admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Lector)
admin.site.register(Corpus)
admin.site.register(Auditorium)
admin.site.register(Discipline)
admin.site.register(Group)
