import prettytable as prettytable
import random as rnd

from univer_structure.models import Auditorium, Lector, Discipline as DisciplineModel, Department as DepartmentModel, \
    Group as GroupModel, Profile as ProfileModel, Specialty as SpecialtyModel, Faculty as FacultyModel
from schedule.models import Times, DisciplineLessons as DisciplineLessonsModel

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
        self._profiles = self.select_profiles()
        self._specialties = self.select_specialties()
        self._faculties = self.select_faculties()

        self._numberOfClasses = 0

        # количество пар зависит от того, сколько дисциплин в кафедрах чтоли?
        # (есть группы в которых есть дисциплины и они повторяются)
        # нужно этот цикл добавить в цикл групп
        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_disciplines()) # у groups[i].get_disciplines() метода нету

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
            return_rooms.append(Room(room.name, room.capacity))
        return return_rooms

    def select_meeting_times(self):
        meeting_times = Times.objects.all()
        return_meeting_times = []
        for time in meeting_times:
            return_meeting_times.append(MeetingTime(time.id, time.times))
        return return_meeting_times

    def select_instructors(self):
        instructors = Lector.objects.all()
        return_instructors = []
        for instructor in instructors:
            return_instructors.append(Instructor(instructor.id, instructor.profile.user.last_name))
        return return_instructors

    def select_groups(self):
        groups = GroupModel.objects.all()
        lector = Lector.objects.filter(disciplines__lectordisciplines__profile_id=1)
        returngroups = []
        for gr in groups:
            returngroups.append(Group(gr.id, gr.name, gr.students, self.select_group_disciplines(gr.id,
                                                                   self.select_group_lectors(gr.id))))
        return returngroups



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

    """
    def get_corpuses(self):
        return self._corpuses """

    def get_instructors(self):
        return self._instructors

    def get_disciplines(self):
        return self._disciplines

    def get_departments(self):
        return self._depts

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

class ScheduleItem:

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
        if (self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        groups = self.data.get_groups()  # data to pick up all the departments
        for gr in groups:
            courses = gr.get_courses()  # pick up the disciplines in each department
            for ds in courses:
                newClass = Class(self._classNumb, gr[ds],
                                 courses[ds])  # for each course we instantiate a new class
                self._classNumb += 1

                newClass.set_meetingTime(
                    self.data.get_meetingTimes()[rnd.randrange(0, len(self.data.get_meetingTimes()))])
                newClass.set_room(self.data.get_rooms()[rnd.randrange(0, len(self.data.get_rooms()))])
                newClass.set_instructor(
                    disciplines[j].get_instructors()[rnd.randrange(0, len(disciplines[j].get_instructors()))])
                self._classes.append(newClass)  # we put the "newClass" instance in this ScheduleItem
        return self

    def calculate_fitness(self):  # calculate and return the fitness
        self._numbOfConflicts = 0
        classes = self.get_classes()

        for i in range(0, len(classes)):
            if (classes[i].get_room().get_seatingCapacity() < classes[
                i].get_discipline().get_maxNumbOfStudents()):  # get_maxNumbOfStudents I deleted
                self._numbOfConflicts += 1

            for j in range(0, len(classes)):
                if (j >= i):
                    if (classes[i].get_meetingTime() == classes[j].get_meetingTime() and
                            classes[i].get_id() != classes[j].get_id()):

                        # if the room is scheduled for more than 1 class at the same meeting time
                        if (classes[i].get_room() == classes[j].get_room()):
                            self._numbOfConflicts += 1

                        # if the instructor is scheduled to teach more than one class at the same meeting time
                        if (classes[i].get_instructor() == classes[j].get_instructor()):
                            self._numbOfConflicts += 1

        return 1 / ((1.0 * self._numbOfConflicts + 1))

    # returns all the classes in this schedule separated by comas
    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) - 1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes) - 1])
        return returnValue


class Population:
    def __init__(self, size, data):
        self._size = size  # size of the population
        self.data = data  # ???don't know why this should be needed?
        self._schedules = []  # population schedules we have get method for that

        for i in range(0, size):
            # giving a size of the population we instantiate schedules
            # and call initialize method on each and put them in schedules
            self._schedules.append(ScheduleItem(self.data).initialize())

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
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[1]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverScheduleItem = ScheduleItem(self.data).initialize()
        for i in range(0, len(crossoverScheduleItem.get_classes())):
            if (rnd.random() > 0.5):
                crossoverScheduleItem.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverScheduleItem.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverScheduleItem

    def _mutate_schedule(self, mutateScheduleItem):
        schedule = ScheduleItem(self.data).initialize()
        for i in range(0, len(mutateScheduleItem.get_classes())):
            if (MUTATION_RATE > rnd.random()): mutateScheduleItem.get_classes()[i] = schedule.get_classes()[i]
        return mutateScheduleItem

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

    def __init__(self, id, name):
        self._id = id  # number of the course
        self._name = name  # name of the course

    def get_number(self):
        return self._id

    def get_name(self):
        return self._name

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
    def __init__(self, id, name, n_students, disciplines, lectors):
        self.id = id
        self.name = name
        self.students = n_students
        self.disciplines = disciplines
        self.lectors = lectors


    def get_id(self):
        return self.id

    def get_group(self):
        return self.name

    def get_number_of_studetns(self):
        return self.students

    def get_disciplines(self):
        return self.disciplines

    def get_lectors(self):
        return self.lectors


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
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity

    def get_number(self):
        return self._number

    def get_seatingCapacity(self):
        return self._seatingCapacity


class MeetingTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time

    def get_id(self): return self._id

    def get_time(self): return self._time


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

    def __init__(self, id, group, discipline, instructor):
        self._id = id
        self._discipline = discipline
        self._group = group
        self._instructor = instructor
        self._meetingTime = None
        self._room = None

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

    def __str__(self):
        return str(self._meetingTime.get_id()) + "," + str(self._discipline.get_number()) + "," + \
               str(self._room.get_number()) + "," + str(self._instructor.get_id()) + ","  # need tp add group

        # each class will be the Department name, the Course number, Room Number, instructor_id (why?), meeting time
        """return str(self._dept.get_name()) + "," +  str(self._discipline.get_number()) + "," + \
               str(self._room.get_number()) + "," + str(self._instructor.get_id()) + "," + str(self._meetingTime.get_id())"""


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
        availableCourseTable = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'instructors'])
        disciplines = self.data.get_disciplines()
        for i in range(0, len(disciplines)):
            instructors = disciplines[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCourseTable.add_row(
                [disciplines[i].get_number(), disciplines[i].get_name(), str(disciplines[i].get_maxNumbOfStudents()),
                 tempStr])  # get_maxNumbOfStudents()
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
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        print(availableMeetingTimeTable)

    def print_generation(self, population):  # prints generation
        table1 = prettytable.PrettyTable(
            ['schedule #', 'fitness', '# of conflicts', 'classes [dept,class,room,instructor,meeting-time]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i + 1), round(schedules[i].get_fitness(), 3), schedules[i].get_numbOfConflicts(),
                            schedules[i].__str__()])
        print(table1)

    def print_schedule_as_table(self, schedule):  # Prints the schedule as a table
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(
            ['Class #', 'Dept', 'Course (number, max # of students)', 'Room (Capacity)', 'Instructor (Id)',
             'Meeting Time (Id)'])
        for i in range(0, len(classes)):
            table.add_row(
                [str(i + 1), str(classes[i].get_dept().get_name()), str(classes[i].get_discipline().get_name()) + " (" +
                 str(classes[i].get_discipline().get_number()) + ", " +
                 str(classes[i].get_discipline().get_maxNumbOfStudents()) + ")",
                 str(classes[i].get_room().get_number()) + " (" + str(
                     classes[i].get_room().get_seatingCapacity()) + ")",
                 classes[i].get_instructor().get_name() + " (" + str(classes[i].get_instructor().get_id()) + ")",
                 classes[i].get_meetingTime().get_time() + " (" + str(classes[i].get_meetingTime().get_id()) + ")"])
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

    geneticAlgorithm = GeneticAlgorithm(data)
    while (population.get_schedules()[0].get_fitness() == 1.0):
        generationNumber += 1
        print("\n> Generation # " + str(generationNumber))

        # we evovle the population from one generation to the next
        # until we get to a population where the fittest schedule has zero (0) conflicts
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        displayMgr.print_generation(population)
        displayMgr.print_schedule_as_table(population.get_schedules()[0])

    print("\n\n")
