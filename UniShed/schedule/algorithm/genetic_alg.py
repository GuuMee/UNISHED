import concurrent.futures
import time

import prettytable as prettytable
import random as rnd

from univer_structure.models import Auditorium, Lector, Discipline as DisciplineModel, Department as DepartmentModel, \
    Group as GroupModel, Profile as ProfileModel, Specialty as SpecialtyModel, Faculty as FacultyModel
from schedule.models import Times, DisciplineLessons as DisciplineLessonsModel, CourseScheduleItem

POPULATION_SIZE = 5
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class DBMgr:
    def __init__(self):
        self._rooms = self.select_rooms()
        self._meetingTimes = self.select_meeting_times()
        self._instructors = self.select_instructors()
        self._disciplines = self.select_disciplines()
        self._depts = self.select_depts()
        self._groups = self.select_groups()
        # self._profiles = self.select_profiles()
        self._profiles = []
        # self._specialties = self.select_specialties()
        self._specialties = []
        # self._faculties = self.select_faculties()
        self._faculties = []
        self._class_types = [t.value for t in CourseScheduleItem.TypesOfClass]

        self._numberOfClasses = 0

        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_disciplines())

    def select_profiles(self):
        profiles = ProfileModel.objects.all()
        returnprofiles = []
        for prof in profiles:
            returnprofiles.append(Profile(prof.id, prof.name))
        return returnprofiles

    def select_specialties(self):
        specialties = SpecialtyModel.objects.filter(profiles__isnull=False)
        return_specs = []
        for spec in specialties:
            return_specs.append(Specialty(spec.id, spec.name, self.select_profiles()[spec]))
        return return_specs

    def select_faculties(self):
        faculties = FacultyModel.objects.filter(specialties__isnull=False)
        return_faculties = []
        for fc in faculties:
            return_faculties.append(Faculty(fc.id, fc.name, self.select_specialties()[fc]))

    def select_rooms(self):
        rooms = Auditorium.objects.all()
        return_rooms = []
        for room in rooms:
            return_rooms.append(Room(room.id, room.name, room.capacity, room.dept.id))
        return return_rooms

    def select_meeting_times(self):
        meeting_times = Times.objects.all()
        return_meeting_times = []
        for time in meeting_times:
            return_meeting_times.append(MeetingTime(time.id, time.time, time.day, time.week_type))
        return return_meeting_times

    def select_instructors(self):
        instructors = Lector.objects.all()
        return_instructors = []
        for instructor in instructors:
            return_instructors.append(Instructor(instructor.id, instructor.profile.user.last_name))
        return return_instructors

    def select_depts(self):
        depts = DepartmentModel.objects.filter(disciplines__disciplinelessons__isnull=False).distinct()
        returnDepts = []
        for dept in depts:
            returnDepts.append(Department(dept.id, self.select_dept_disciplines(dept.name)))
        return returnDepts

    def select_dept_disciplines(self, deptName):
        ds_numbers = DisciplineLessonsModel.objects.filter(discipline__department__name=deptName).values_list('id', flat=True)
        return_value = []
        for ds in self._disciplines:
            if ds.get_number() in ds_numbers:
                return_value.append(ds)
        return return_value

    def select_disciplines(self):
        disciplines = DisciplineLessonsModel.objects.all()
        return_disciplines = []
        for ds in disciplines:
            return_disciplines.append(Discipline(
                ds.id,
                ds.discipline.name,
                ds.discipline.department.id,
                ds.lecture,
                ds.practice,
                ds.laboratory,
                25,  # needs to be changed to ds.group.students.count()
            ))
        return return_disciplines

    def select_groups(self):
        groups = GroupModel.objects.all()
        return_groups = []
        for group in groups:
            db_disciplines = DisciplineLessonsModel.objects.filter(group=group).values_list('id', flat=True)
            disciplines = []
            for ds in self._disciplines:
                if ds.get_number() in db_disciplines:
                    disciplines.append(ds)
            return_groups.append(Group(
                id=group.id,
                name=group.name,
                n_students=25,  # needs to be changed to group.students.count()
                disciplines=disciplines)
            )
        return return_groups

    def select_discipline_instructor(self, courseNumber):
        lector = DisciplineLessonsModel.objects.get(id=courseNumber).lector
        returnValue = None
        for i in range(0, len(self._instructors)):
            if self._instructors[i].get_id() == lector.id:
                returnValue = self._instructors[i]
        return returnValue

    def get_dept_rooms(self, dept):
        rooms = []
        for room in self._rooms:
            if room.get_department() == dept:
                rooms.append(room)
        return rooms

    def select_group_discipline_lector(self ):
        discip = DisciplineLessonsModel.objects.all()
        return_discipline = []
        for di in discip:
            return_discipline.append(Course(di.id, di.discipline, di.lector, di.group))
        return return_discipline

    def select_group_lectors(self, group_id):
        group_lectors = Lector.objects.filter(lessonlectors__groupslessons__id=group_id)
        return_gr_lectors = []
        for gr in group_lectors:
            return_gr_lectors.append(gr)
        return return_gr_lectors


    def get_rooms(self):
        return self._rooms


    def get_instructors(self):
        return self._instructors

    def get_disciplines(self):
        return self._disciplines

    def get_departments(self):
        return self._depts

    def get_odd_meeting_times(self):
        times = []
        for time in self._meetingTimes:
            if time.get_week() == Times.WeekOfStudy.ODD_WEEK:
                times.append(time)
        return times

    def get_even_meeting_times(self):
        times = []
        for time in self._meetingTimes:
            if time.get_week() == Times.WeekOfStudy.EVEN_WEEK:
                times.append(time)
        return times

    def get_meetingTimes(self):
        return self._meetingTimes

    def get_numberOfClasses(self):
        return self._numberOfClasses

    def get_groups(self):
        return self._groups

    def get_profiles(self):
        return self._profiles

    def get_specialties(self):
        return self._specialties

    def get_faculties(self):
        return self._faculties

    def get_class_types(self):
        return self._class_types


class Schedule:

    def __init__(self, data):
        self.data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0  # class number counter
        self._isFitnessChanged = True

    def get_classes(self):  # get method for classes
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self):
        return self._numbOfConflicts

    def get_fitness(self):  # the fitness for this schedule
        if self._isFitnessChanged == True:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def create_classes(self, group, discipline, class_type):
        classes = []
        hours = getattr(discipline, class_type)
        lector = self.data.select_discipline_instructor(discipline.get_number())
        class_1 = Class(self._classNumb, group, discipline, lector, class_type)
        rooms = self.data.get_dept_rooms(discipline.get_department())
        selected_room = rooms[rnd.randrange(0, len(rooms))]
        class_1.set_room(selected_room)
        if hours == 18:
            meeting_times = self.data.get_meetingTimes()
            class_1.set_meetingTime(meeting_times[rnd.randrange(0, len(meeting_times))])
            classes.append(class_1)
            self._classNumb += 1
        elif hours >= 36:
            odd_meeting_times = self.data.get_odd_meeting_times()
            class_1.set_meetingTime(odd_meeting_times[rnd.randrange(0, len(odd_meeting_times))])
            classes.append(class_1)
            self._classNumb += 1

            class_2 = Class(self._classNumb, group, discipline, lector, class_type)
            class_2.set_room(selected_room)
            even_meeting_times = self.data.get_even_meeting_times()
            class_2.set_meetingTime(even_meeting_times[rnd.randrange(0, len(even_meeting_times))])
            classes.append(class_2)
            self._classNumb += 1

        if hours >= 54:
            class_3 = Class(self._classNumb, group, discipline, lector, class_type)
            class_3.set_room(selected_room)
            meeting_times = self.data.get_meetingTimes()
            class_3.set_meetingTime(meeting_times[rnd.randrange(0, len(meeting_times))])
            classes.append(class_3)
            self._classNumb += 1

        return classes

    def initialize(self):
        groups = self.data.get_groups()
        for group in groups:
            for ds in group.get_disciplines():
                for class_type in self.data.get_class_types():

                    # with concurrent.futures.ThreadPoolExecutor(
                    #         max_workers=POPULATION_SIZE - NUMB_OF_ELITE_SCHEDULES) as executor:
                    #     executor.map(self )

                    if getattr(ds, class_type):
                        classes = self.create_classes(group, ds, class_type)
                        self._classes += classes
        return self

    def calculate_fitness(self):  # calculate and return the fitness
        self._numbOfConflicts = 0
        classes = self.get_classes()

        for i in range(0, len(classes)):
            if (classes[i].get_room().get_seatingCapacity() < classes[i].get_discipline().get_num_students()):
                self._numbOfConflicts += 1

            for j in range(i+1, len(classes)):
                #if ( classes[i].get_discipline() == classes[j].get_discipline() and
                    #classes[i].get_class_type() == classes[j].get_class_type() and not
                        #classes[i].get_room() != classes[j].get_room()):
                    #self._numbOfConflicts += 1
                if (classes[i].get_meetingTime() == classes[j].get_meetingTime() and
                        classes[i].get_id() != classes[j].get_id()):

                    # if the room is scheduled for more than 1 class at the same meeting time
                    if (classes[i].get_room() == classes[j].get_room()):
                        self._numbOfConflicts += 1

                    # if the instructor is scheduled to teach more than one class at the same meeting time
                    if (classes[i].get_instructor() == classes[j].get_instructor()):
                        self._numbOfConflicts += 1

                    if (classes[i].get_group() == classes[j].get_group()):
                        self._numbOfConflicts += 1

        return 1 / ((1.0 * self._numbOfConflicts + 1))

    # returns all the classes in this schedule separated by comas
    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) - 1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes) - 1])
        return returnValue

    def save(self):
        for klass in self._classes:
            klass.save()


class Population:
    def __init__(self, size, data):
        self._size = size  # size of the population
        self.data = data
        self._schedules = []  # population schedules we have get method for that

        for i in range(0, size):
            # giving a size of the population we instantiate schedules
            # and call initialize method on each and put them in schedules
            self._schedules.append(Schedule(self.data).initialize())

    def get_schedules(self):  # ???what can we use instead of this get method???
        return self._schedules


class GeneticAlgorithm:
    def __init__(self, data):
        self.data = data

    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0, self.data)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            tournament_pop = self._select_tournament_population(pop)
            schedule1 = tournament_pop.get_schedules()[0]
            schedule2 = tournament_pop.get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop


    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    """
    def _mutate_population(self, population):
        with concurrent.futures.ThreadPoolExecutor(max_workers=POPULATION_SIZE - NUMB_OF_ELITE_SCHEDULES) as executor:
            executor.map(self._mutate_schedule, population.get_schedules()[NUMB_OF_ELITE_SCHEDULES:POPULATION_SIZE])
        return population
    """

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule(self.data).initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            # with concurrent.futures.ThreadPoolExecutor(
            #         max_workers=POPULATION_SIZE - NUMB_OF_ELITE_SCHEDULES) as executor:
            #     executor.map(self._crossover_schedule)
            if (rnd.random() > 0.5):
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule(self.data).initialize()

        for i in range(0, len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0, self.data)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Course:

    def __init__(self, number, discipline, instructor, group):
        self._number = number
        self._discipline = discipline
        self._instructor = instructor
        self._group = group

    def get_number(self): return self._number
    def get_discipline(self): return self._discipline
    def get_instructor(self): return self._instructor
    def get_group(self): return self._group
    def __str__(self):
        return "{} - {} -{} ".format(self._group, self._discipline, self._instructor)


class Discipline:

    def __init__(self, id, name, department, lecture, practice, laboratory, n_students):
        self._id = id
        self._name = name
        self._department = department
        self.lecture = lecture
        self.practice = practice
        self.laboratory = laboratory
        self.n_students = n_students

    def get_number(self):
        return self._id

    def get_name(self):
        return self._name

    def get_department(self):
        return self._department

    def get_num_students(self):
        return self.n_students

    def __str__(self):
        return self._name


class DisciplineClass:
    def __init__(self, name, lecture, practice, laboratory):
        self.name = name
        self.lecture = lecture
        self.practice = practice
        self.laboratory = laboratory

    def get_name(self):
        return self.name

    def get_lecture(self):
        return "Лк - {}".format(self.name)

    def set_practice(self):
        return "Пр - {}".format(self.name)

    def set_laboratory(self):
        return "Лб - {}".format(self.name)


class Group:
    def __init__(self, id, name, n_students, disciplines):
        self.id = id
        self.name = name
        self.students = n_students
        self.disciplines = disciplines

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_number_of_students(self):
        return self.students

    def get_disciplines(self):
        return self.disciplines


class Instructor:

    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def __str__(self):
        return self._name


class Room:
    def __init__(self, id, number, seatingCapacity, department):
        self._id = id
        self._number = number
        self._seatingCapacity = seatingCapacity
        self._department = department

    def get_id(self):
        return self._id

    def get_number(self):
        return self._number

    def get_seatingCapacity(self):
        return self._seatingCapacity

    def get_department(self):
        return self._department


class MeetingTime:
    def __init__(self, id, time, day, week):
        self._id = id
        self._time = time
        self._day = day
        self._week = week

    def get_id(self): return self._id

    def get_time(self): return self._time

    def get_day(self): return self._day

    def get_week(self): return self._week

    def __str__(self):
        return '{}: {}, {}'.format(self._day, self._time, self._week)


class Department:
    def __init__(self, name, disciplines):
        self._name = name
        self._disciplines = disciplines

    def get_name(self): return self._name

    def get_disciplines(self): return self._disciplines


class Profile:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self): return self._id
    def get_name(self): return self._name


class Specialty:
    def __init__(self, id, name, profiles):
        self.id = id
        self._name = name
        self._profiles = profiles

    def get_id(self): return self._id

    def get_name(self): return self._name

    def get_profiles(self): return self._profiles


class Faculty:
    def __init__(self, id, name, specialties):
        self._id = id
        self._name = name
        self._specialties = specialties

    def get_id(self): return self._id

    def get_name(self): return self._name

    def get_specialties(self): return self._specialties


class Class:  # Пара

    def __init__(self, id, group, discipline, instructor, class_type):
        self._id = id
        self._discipline = discipline
        self._group = group
        self._instructor = instructor
        self._meetingTime = None
        self._room = None
        self._class_type = class_type

    def get_id(self):
        return self._id

    def get_discipline(self):
        return self._discipline

    def get_group(self):
        return self._group

    def get_instructor(self):
        return self._instructor

    def get_meetingTime(self):
        return self._meetingTime

    def get_room(self):
        return self._room

    def set_meetingTime(self, meetingTime):
        self._meetingTime = meetingTime

    def set_room(self, room):
        self._room = room

    def get_class_type(self):
        return self._class_type

    def save(self):
        CourseScheduleItem.objects.create(
            class_type=self._class_type,
            time_id=self._meetingTime.get_id(),
            auditorium_id=self._room.get_id(),
            lector_id=self._instructor.get_id(),
            discipline=DisciplineModel.objects.get(disciplinelessons__group_id=self._group.get_id(), disciplinelessons__id=self._discipline.get_number()),
            group_id=self._group.get_id()
        )

    def __str__(self):
        return str(self._meetingTime.get_id()) + "," + str(self._discipline.get_number()) + "," + \
               str(self._room.get_number()) + "," + str(self._instructor.get_id()) + ","


class DisplayMgr:  # display manager class
    def __init__(self, data):
        self.data = data

    def print_available_data(self):
        print("> All Available Data")
        self.print_dept()
        self.print_discipline()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()

    # that prints the department, the course, the instructor, the room, the meeting time

    def print_dept(self):
        depts = self.data.get_departments()
        availableDeptsTable = prettytable.PrettyTable(['dept', 'disciplines'])
        for i in range(0, len(depts)):
            disciplines = depts.__getitem__(i).get_disciplines()
            tempStr = "["
            for j in range(0, len(disciplines) - 1):
                tempStr += disciplines[j].__str__() + ", "
            tempStr += disciplines[len(disciplines) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)

    def print_discipline(self):
        availableCourseTable = prettytable.PrettyTable(['id', 'course', 'instructors'])
        disciplines = self.data.get_disciplines()
        for i in range(0, len(disciplines)):
            # instructors = disciplines[i].get_instructors()
            instructors = [self.data.select_discipline_instructor(disciplines[i].get_number())]
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCourseTable.add_row(
                [disciplines[i].get_number(), disciplines[i].get_name(), tempStr])
        print(availableCourseTable)

    def print_instructor(self):
        availableInstructorsTable = prettytable.PrettyTable(['id', 'instructor'])
        instructors = self.data.get_instructors()
        for i in range(0, len(instructors)):
            availableInstructorsTable.add_row([instructors[i].get_id(), instructors[i].get_name()])
        print(availableInstructorsTable)

    def print_room(self):
        availableRoomsTable = prettytable.PrettyTable(['room #', 'max seating capacity'])
        rooms = self.data.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)

    def print_meeting_times(self):
        availableMeetingTimeTable = prettytable.PrettyTable(['id', 'Meeting Time'])
        meetingTimes = self.data.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(), str(meetingTimes[i])])
        print(availableMeetingTimeTable)

    def print_generation(self, population):  # prints generation
        table1 = prettytable.PrettyTable(
            ['# расписания', 'фитнес', '# конфликтов', 'хромосомы - занятия[кафедра, занятие, аудитория,преподаватель,время]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i + 1), round(schedules[i].get_fitness(), 3), schedules[i].get_numbOfConflicts(),
                            schedules[i].__str__()])
        print(table1)

    def print_schedule_as_table(self, schedule):  # Prints the schedule as a table
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(
            ['Пара # (тип)', 'Группа', 'Дисциплины (id, # количество студентов группы`)', 'Аудитория (Вместимость)', 'Преподаватель (Id)',
             'Время занятий (Id)'])
        for i in range(0, len(classes)):
            table.add_row(
                [str(i + 1) + "(" + classes[i].get_class_type() + ")",
                 str(classes[i].get_group().get_name()),
                 str(classes[i].get_discipline().get_name()) + " (" + str(classes[i].get_discipline().get_number()) + ", " +
                 str(classes[i].get_discipline().get_num_students()) + ")",
                 str(classes[i].get_room().get_number()) + " (" + str(
                     classes[i].get_room().get_seatingCapacity()) + ")",
                 classes[i].get_instructor().get_name() + " (" + str(classes[i].get_instructor().get_id()) + ")",
                 str(classes[i].get_meetingTime()) + " (" + str(classes[i].get_meetingTime().get_id()) + ")"])
        print(table)


def run():
    data = DBMgr()
    displayMgr = DisplayMgr(data)
    displayMgr.print_available_data()
    generationNumber = 0
    print("\n> Generation # " + str(generationNumber))

    # instantiating the population
    population = Population(POPULATION_SIZE, data)

    # this code sorts the schedules in the population
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

    # this will print generation zero (0), because generationNumber = 0
    displayMgr.print_generation(population)


    # fittest schedule in that generation in table format
    displayMgr.print_schedule_as_table(population.get_schedules()[0])

    start_time = time.time()



    geneticAlgorithm = GeneticAlgorithm(data)
    while population.get_schedules()[0].get_fitness() < 1.0:
        generationNumber += 1
        print("\n> Поколение # " + str(generationNumber))
        per_gen = time.time()
        # мы эволюционируем популяцию с одного поколения в другое
        # пока мы не придём к популяции, где функция приспособленности расписания будет иметь (0) конфликтов
        population = geneticAlgorithm.evolve(population)

        # применение многопоточности
        with concurrent.futures.ThreadPoolExecutor(
              max_workers=POPULATION_SIZE - NUMB_OF_ELITE_SCHEDULES) as executor:
            executor.map(population, population.get_schedules()[NUMB_OF_ELITE_SCHEDULES:POPULATION_SIZE])

        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

        print("ВЫПОЛНЕНИЕ ОДНОГО ПОКОЛЕНИЯ:--- %s секунд ---" % (time.time() - per_gen))
        print("ОБЩЕЕ ВЫПОЛНЕНИЕ:--- %s секунд ---" % (time.time() - start_time))
        displayMgr.print_generation(population)
        displayMgr.print_schedule_as_table(population.get_schedules()[0])

        # with concurrent.futures.ThreadPoolExecutor(
        #         max_workers=POPULATION_SIZE - NUMB_OF_ELITE_SCHEDULES) as executor:
        #     executor.map(displayMgr.print_generation, population.get_schedules()[NUMB_OF_ELITE_SCHEDULES:POPULATION_SIZE])




    population.get_schedules()[0].save()

    print("\n\n")
