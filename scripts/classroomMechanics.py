import re
import DataStructures as ds

class Student:
    def __init__(self, id, year, major, preferredClassMajor, accomodations, name=-1):
        self.id = id
        self.year = year
        self.major = major
        self.prefMajor = preferredClassMajor
        self.accomodations = accomodations
        self.name = name

    def __lt__(self, other):
        if self.major == other.major:
            #if both have same major, just compare by class years
            return self.year < other.year
        elif self.major == self.prefMajor:
            #if both have different majors, but self has major that matches preferred class, then 
            #self is ranked greater (i.e. not less) than other
            return False
        elif other.major == other.prefMajor:
            #if both have different majors, but other has major that matches preferred class, then
            #self is ranked less than other
            return True
        else:
            #else if neither have majors that match preferred class major, then simply rank by greatest school year
            return self.year < other.year
    
    def __gt__(self, other):
        if self.major == other.major:
            #if both have same major, just compare by class years
            return self.year > other.year
        elif self.major == self.prefMajor:
            #if both have different majors, but self has major that matches preferred class, then 
            #self is ranked greater than other
            return True
        elif other.major == other.prefMajor:
            #if both have different majors, but other has major that matches preferred class, then
            #self is ranked less than (i.e. not greater than) other
            return False
        else:
            #else if neither have majors that match preferred class major, then simply rank by greatest school year
            return self.year > other.year
    
    def __eq__(self, other):
        if self.major != self.prefMajor and other.major != other.prefMajor:
            return self.year == other.year
        else:
            return self.major == other.major and self.year == other.year

    def __ne__(self, other):
        if self.major != self.prefMajor and other.major != other.prefMajor:
            return self.year != other.year
        else:
            return self.major != other.major or self.year == other.year

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other

    def __str__(self):
        if self.name == -1:
            return f"{self.id}"
        else:
            return f"{self.name}"

class Class:
    def __init__(self, class_name, requiredProfessor, majorContributedTo, domainCanBeTaughtIn, isEsem, id=-1, sections=1):
        self.name = class_name
        self.enrolled = []
        self.professor = requiredProfessor
        self.time = -1
        self.room = -1
        self.preferredStudents = 0
        self.major = majorContributedTo
        self.domain = domainCanBeTaughtIn
        self.needsAccessibility = False
        self.isEsem = isEsem
        self.id = id
        self.sections = sections
    
    def notFull(self):
        return self.len(self.enrolled) - self.roomSize != 0

    def __gt__(self, other):
        return self.preferredStudents > other.preferredStudents
    
    def __lt__(self, other):
        return self.preferredStudents < other.preferredStudents

    def __ge__(self, other):
        return self.preferredStudents >= other.preferredStudents

    def __le__(self, other):
        return self.preferredStudents <= other.preferredStudents

    def __eq__(self, other):
        return self.preferredStudents == other.preferredStudents

    def __ne__(self, other):
        return self.preferredStudents != other.preferredStudents

    def __str__(self):
        students = ""
        for s in self.enrolled:
            students += f"{s} "
        return f"{self.name}\t{self.room}\t{self.professor}\t{self.time}\t{students}"

class professor:
    def __init__(self, profName, id):
        self.name = profName
        self.id = id
    def __str__(self):
        return f"Professor Name: {self.name} ID: {self.id}"

class domain:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __str__(self):
        return f"{self.name}, {self.id}"

class TimeSlot:
    def __init__(self, id, start_time, end_time, days_of_week):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.days_of_week = days_of_week

    def __str__(self):
        return f"{self.id}: {self.start_time} - {self.end_time}"

    def schedule_conflict(self, LL):
        loc = LL.head

        if loc is None:
            return False
        
        while not loc is None:
            if(self.conflicts_with(loc.data)):
                return True
            loc = loc.next

        return False

    def conflicts_with(self, other):
        #       --self--
        #   -----other------
        if other.start_time <= self.start_time <= self.end_time <= other.end_time:
            for self_day in self.days_of_week:
                if other.days_of_week.count(self_day) > 0:
                    return True
        #   ----self----
        #       ----other----
        if other.start_time <= self.end_time <= other.end_time:
            for self_day in self.days_of_week:
                if self_day in self.days_of_week:
                    if other.days_of_week.count(self_day) > 0:
                        return True
        
        #       ---self---
        #   ---other---
        if self.start_time <= other.end_time <= self.end_time:
            for self_day in self.days_of_week:
                if self_day in self.days_of_week:
                    if other.days_of_week.count(self_day) > 0:
                        return True
        
        #   --------self--------
        #       ---other---
        if self.start_time <= other.start_time <= other.end_time <= self.end_time:
            for self_day in self.days_of_week:
                if self_day in self.days_of_week:
                    if other.days_of_week.count(self_day) > 0:
                        return True

        return False


class Time:
    def __init__(self, stringTime):
        self.time = self.initialize(stringTime)

    def __str__(self):
        return f"{self.time}"

    def initialize(self, stringTime):
        parts = stringTime.split(' ')
        morning = True
        if parts[1] == 'PM':
            morning = False
        hourMin = parts[0].split(':')
        hour = int(hourMin[0])
        if not morning:
            hour += 12
        min = int(hourMin[1])
        return float(hour) + float(min)/60

    def __le__(self, other):
        return self.time <= other.time
    
    def __ge__(self, other):
        return self.time >= other.time

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time

    def __eq__(self, other):
        return self.time == other.time

    def __ne__(self, other):
        return self.time != other.time


class Room:
    def __init__(self, id, capacity, domain, accessible, name=""):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.domain = domain
        self.accessible = accessible

    def __gt__(self, other):
        return self.capacity > other.capacity

    def __lt__(self, other):
        return self.capacity < other.capacity

    def __eq__(self, other):
        return self.capacity == other.capacity

    def __ne__(self, other):
        return self.capacity != other.capacity

    def __ge__(self, other):
        return self.capacity >= other.capacity

    def __le__(self, other):
        return self.capacity <= other.capacity

    def __str__(self):
        return f"{self.id}"


def printClassArray(arr):
    print("[",end="")
    for i in arr:
        if not i is None:
            print(f"{i.name} ", end="")
        else:
            print(f"None ", end="")
    print("]")

def printRoomArray(arr):
    print("[",end="")
    for i in arr:
        if not i is None:
            print(f"{i.id}-{i.capacity} ", end="")
        else:
            print(f"None ", end="")
    print("]")
