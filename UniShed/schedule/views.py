from django.db.models import Count, Case, When, Value, BooleanField, Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView
from functools import reduce
from operator import or_

from schedule.models import CourseScheduleItem, Times
from univer_structure.models import Group, Lector, Auditorium


class CourseScheduleView(ListView):
    model = CourseScheduleItem
    template_name = 'schedule/schedule_table.html'


@login_required
def student_schedule_view(request):
    user = request.user
    student = user.profile.student
    group = student.group
    context = {
        "odd_monday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.MONDAY,
                                                         time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_tuesday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.TUESDAY,
                                                          time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_wednesday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.WEDNESDAY,
                                                            time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_thursday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.THURSDAY,
                                                           time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_friday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.FRIDAY,
                                                         time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_saturday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.SATURDAY,
                                                           time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "even_monday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.MONDAY,
                                                        time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_tuesday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.TUESDAY,
                                                         time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_wednesday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.WEDNESDAY,
                                                           time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_thursday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.THURSDAY,
                                                          time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_friday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.FRIDAY,
                                                        time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_saturday": CourseScheduleItem.objects.filter(group_id=group.id, time__day=Times.DayOfStudy.SATURDAY,
                                                        time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "group": group,
        "student": student,
    }
    return render(request, "schedule/student_index.html", context)


@login_required
def lector_schedule_view(request):
    user = request.user
    lector = user.profile.lector

    context = {
        "odd_monday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.MONDAY,
                                                        time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_tuesday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.TUESDAY,
                                                         time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_wednesday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.WEDNESDAY,
                                                           time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_thursday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.THURSDAY,
                                                          time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_friday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.FRIDAY,
                                                        time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_saturday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.SATURDAY,
                                                          time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "even_monday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.MONDAY,
                                                         time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_tuesday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.TUESDAY,
                                                          time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_wednesday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.WEDNESDAY,
                                                            time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_thursday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.THURSDAY,
                                                           time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_friday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.FRIDAY,
                                                         time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_saturday": CourseScheduleItem.objects.filter(lector_id=lector.id, time__day=Times.DayOfStudy.SATURDAY,
                                                           time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "lector": lector
    }
    return render(request, "schedule/lector_index.html", context)


def find_conflicts(schedules):
    conflict_ids = []
    conflict1 = schedules.values('auditorium', 'time').annotate(count=Count('id')).order_by().filter(count__gt=1)
    conflict2 = schedules.values('lector', 'time').annotate(count=Count('id')).order_by().filter(count__gt=1)
    conflict3 = schedules.values('group', 'time').annotate(count=Count('id')).order_by().filter(count__gt=1)

    conflict1_objs = schedules.none()
    if conflict1.count() > 0:
        query1 = reduce(or_, (Q(auditorium=row['auditorium'], time=row['time']) for row in conflict1))
        conflict1_objs = schedules.filter(query1)

    conflict2_objs = schedules.none()
    if conflict2.count() > 0:
        query2 = reduce(or_, (Q(lector=row['lector'], time=row['time']) for row in conflict2))
        conflict2_objs = schedules.filter(query2)

    conflict3_objs = schedules.none()
    if conflict3_objs.count() > 0:
        query3 = reduce(or_, (Q(group=row['group'], time=row['time']) for row in conflict3))
        conflict3_objs = schedules.filter(query3)

    conflict_ids += conflict1_objs.values_list('id', flat=True)
    conflict_ids += conflict2_objs.values_list('id', flat=True)
    conflict_ids += conflict3_objs.values_list('id', flat=True)

    schedules = schedules.annotate(has_conflict=Case(
        When(id__in=conflict_ids, then=Value(True)),
        default=Value(False),
        output_field=BooleanField()
    ))

    return schedules


@login_required
def dispatcher_view(request):
    schedules = CourseScheduleItem.objects.all()
    schedules = find_conflicts(schedules)
    groups = Group.objects.all()
    #groups_in_set = set(groups.values("name").all())
    lectors = Lector.objects.all()
    auditoriums = Auditorium.objects.all()
    context = {
        "odd_monday": schedules.filter( time__day=Times.DayOfStudy.MONDAY, time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_tuesday": schedules.filter( time__day=Times.DayOfStudy.TUESDAY,
                                                         time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_wednesday": schedules.filter( time__day=Times.DayOfStudy.WEDNESDAY,
                                                           time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_thursday": schedules.filter( time__day=Times.DayOfStudy.THURSDAY,
                                                          time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_friday": schedules.filter( time__day=Times.DayOfStudy.FRIDAY,
                                                        time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "odd_saturday": schedules.filter( time__day=Times.DayOfStudy.SATURDAY,
                                                          time__week_type=Times.WeekOfStudy.ODD_WEEK),
        "even_monday": schedules.filter( time__day=Times.DayOfStudy.MONDAY,
                                                         time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_tuesday": schedules.filter( time__day=Times.DayOfStudy.TUESDAY,
                                                          time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_wednesday": schedules.filter( time__day=Times.DayOfStudy.WEDNESDAY,
                                                            time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_thursday": schedules.filter( time__day=Times.DayOfStudy.THURSDAY,
                                                           time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_friday": schedules.filter( time__day=Times.DayOfStudy.FRIDAY,
                                                         time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "even_saturday": schedules.filter( time__day=Times.DayOfStudy.SATURDAY,
                                                           time__week_type=Times.WeekOfStudy.EVEN_WEEK),
        "groups": groups,
        #"groups_set":groups_in_set,
        "lectors": lectors,
        "auditoriums": auditoriums,
    }

    return render(request, "schedule/dispatcher_index.html", context)


def sort_schedule(request):
    data = dict()
    if request.method == 'POST':
        schedules = CourseScheduleItem.objects.all()
        group = request.POST.get('group_field_value')
        lector = request.POST.get('lector_field_value')
        auditorium = request.POST.get('room_field_value')
        time = request.POST.get('time_field_value')

        if group and group != 'Группу...':
            schedules = schedules.filter(group__name=group)
        if lector and lector != 'Преподавателя...':
            schedules = schedules.filter(lector_id=int(lector))
        if auditorium and auditorium != 'Аудиторию...':
            schedules = schedules.filter(auditorium__name=auditorium)
        if time and time != 'Время...':
            schedules = schedules.filter(time__time=time)

        schedules = find_conflicts(schedules)
        context = {
            "odd_monday": schedules.filter(time__day=Times.DayOfStudy.MONDAY, time__week_type=Times.WeekOfStudy.ODD_WEEK),
            "odd_tuesday": schedules.filter(time__day=Times.DayOfStudy.TUESDAY, time__week_type=Times.WeekOfStudy.ODD_WEEK),
            "odd_wednesday": schedules.filter(time__day=Times.DayOfStudy.WEDNESDAY, time__week_type=Times.WeekOfStudy.ODD_WEEK),
            "odd_thursday": schedules.filter(time__day=Times.DayOfStudy.THURSDAY, time__week_type=Times.WeekOfStudy.ODD_WEEK),
            "odd_friday": schedules.filter(time__day=Times.DayOfStudy.FRIDAY, time__week_type=Times.WeekOfStudy.ODD_WEEK),
            "odd_saturday": schedules.filter(time__day=Times.DayOfStudy.SATURDAY, time__week_type=Times.WeekOfStudy.ODD_WEEK),
            "even_monday": schedules.filter(time__day=Times.DayOfStudy.MONDAY, time__week_type=Times.WeekOfStudy.EVEN_WEEK),
            "even_tuesday": schedules.filter(time__day=Times.DayOfStudy.TUESDAY, time__week_type=Times.WeekOfStudy.EVEN_WEEK),
            "even_wednesday": schedules.filter(time__day=Times.DayOfStudy.WEDNESDAY, time__week_type=Times.WeekOfStudy.EVEN_WEEK),
            "even_thursday": schedules.filter(time__day=Times.DayOfStudy.THURSDAY, time__week_type=Times.WeekOfStudy.EVEN_WEEK),
            "even_friday": schedules.filter(time__day=Times.DayOfStudy.FRIDAY, time__week_type=Times.WeekOfStudy.EVEN_WEEK),
            "even_saturday": schedules.filter(time__day=Times.DayOfStudy.SATURDAY, time__week_type=Times.WeekOfStudy.EVEN_WEEK),

        }
        data['html_form'] = render_to_string('schedule/select_sort.html', context, request=request)
    return JsonResponse(data)


def annotate_usage_rooms(auditoriums, day, week):
    for auditorium in auditoriums:
        auditorium.times = Times.objects.filter(
            day=day, week_type=week,
            schedule_items__auditorium__pk=auditorium.pk
        ).values_list('time', flat=True).annotate(
            count=Count('id')).order_by()
    return auditoriums


def busy_auditoriums_view(request):
    auditoriums = Auditorium.objects.values_list("name", flat=True)
    auditoriums = set(auditoriums)
    odd_monday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.MONDAY, week=Times.WeekOfStudy.ODD_WEEK)
    odd_tuesday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.TUESDAY, week=Times.WeekOfStudy.ODD_WEEK)
    odd_wednesday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.WEDNESDAY, week=Times.WeekOfStudy.ODD_WEEK)
    odd_thursday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.THURSDAY, week=Times.WeekOfStudy.ODD_WEEK)
    odd_friday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.FRIDAY, week=Times.WeekOfStudy.ODD_WEEK)
    odd_saturday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.SATURDAY, week=Times.WeekOfStudy.ODD_WEEK)

    even_monday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.MONDAY, week=Times.WeekOfStudy.EVEN_WEEK)
    even_tuesday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.TUESDAY, week=Times.WeekOfStudy.EVEN_WEEK)
    even_wednesday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.WEDNESDAY, week=Times.WeekOfStudy.EVEN_WEEK)
    even_thursday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.THURSDAY, week=Times.WeekOfStudy.EVEN_WEEK)
    even_friday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.FRIDAY, week=Times.WeekOfStudy.EVEN_WEEK)
    even_saturday = annotate_usage_rooms(Auditorium.objects.all(), day=Times.DayOfStudy.SATURDAY, week=Times.WeekOfStudy.EVEN_WEEK)
    context = {
        "auditoriums": auditoriums,
        "odd_monday": odd_monday,
        "odd_tuesday": odd_tuesday,
        "odd_wednesday": odd_wednesday,
        "odd_thursday": odd_thursday,
        "odd_friday": odd_friday,
        "odd_saturday": odd_saturday,
        "even_monday": even_monday,
        "even_tuesday": even_tuesday,
        "even_wednesday": even_wednesday,
        "even_thursday": even_thursday,
        "even_friday": even_friday,
        "even_saturday": even_saturday,
    }
    return render(request, "schedule/busy_auditoriums.html", context)


def annotate_usage_lectors(lectors, day, week):
    for lector in lectors:
        lector.times = Times.objects.filter(
            day=day, week_type=week,
            schedule_items__auditorium__pk=lector.pk
        ).values_list('time', flat=True).annotate(
            count=Count('id')).order_by()
    return lectors


def busy_lectors_view(request):
    lectors = Lector.objects.all()
    odd_monday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.MONDAY,
                                      week=Times.WeekOfStudy.ODD_WEEK)
    odd_tuesday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.TUESDAY,
                                       week=Times.WeekOfStudy.ODD_WEEK)
    odd_wednesday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.WEDNESDAY,
                                         week=Times.WeekOfStudy.ODD_WEEK)
    odd_thursday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.THURSDAY,
                                        week=Times.WeekOfStudy.ODD_WEEK)
    odd_friday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.FRIDAY,
                                      week=Times.WeekOfStudy.ODD_WEEK)
    odd_saturday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.SATURDAY,
                                        week=Times.WeekOfStudy.ODD_WEEK)

    even_monday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.MONDAY,
                                       week=Times.WeekOfStudy.EVEN_WEEK)
    even_tuesday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.TUESDAY,
                                        week=Times.WeekOfStudy.EVEN_WEEK)
    even_wednesday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.WEDNESDAY,
                                          week=Times.WeekOfStudy.EVEN_WEEK)
    even_thursday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.THURSDAY,
                                         week=Times.WeekOfStudy.EVEN_WEEK)
    even_friday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.FRIDAY,
                                       week=Times.WeekOfStudy.EVEN_WEEK)
    even_saturday = annotate_usage_lectors(Lector.objects.all(), day=Times.DayOfStudy.SATURDAY,
                                         week=Times.WeekOfStudy.EVEN_WEEK)
    context = {
        "lectors": lectors,
        "odd_monday": odd_monday,
        "odd_tuesday": odd_tuesday,
        "odd_wednesday": odd_wednesday,
        "odd_thursday": odd_thursday,
        "odd_friday": odd_friday,
        "odd_saturday": odd_saturday,
        "even_monday": even_monday,
        "even_tuesday": even_tuesday,
        "even_wednesday": even_wednesday,
        "even_thursday": even_thursday,
        "even_friday": even_friday,
        "even_saturday": even_saturday,
    }
    return render(request, "schedule/busy_lectors.html", context)



