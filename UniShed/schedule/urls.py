from django.urls import path
from . import views

#TEMPLATE URLS!
from .views import CourseScheduleView

app_name = 'schedule'


urlpatterns = [
    path('s_schedule/', views.student_schedule_view, name='student_schedule'),
    path('l_schedule/', views.lector_schedule_view, name='lector_schedule'),
    path('dispatcher/', views.dispatcher_view, name="dispatcher_view"),
    path('sort_group/', views.sort_schedule, name="sort_schedule_view"),
    path("table/", CourseScheduleView.as_view()),
    path('busy_auditoriums/', views.busy_auditoriums_view, name="busy_auditoriums"),
    path('busy_lectors/', views.busy_lectors_view, name="busy_lectors"),
]
