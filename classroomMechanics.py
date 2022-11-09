class Student:
    def __init__(self, id, year, major, preferredClassMajor, accomodations):
        self.id = id
        self.year = year
        self.major = major
        self.prefMajor = preferredClassMajor
        self.accomodations = accomodations

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
        return f"{self.id}"

class Class:
    def __init__(self, class_name, requiredProfessor, majorContributedTo, domainCanBeTaughtIn):
        self.name = class_name
        self.enrolled = []
        self.professor = requiredProfessor
        self.time = -1
        self.room = -1
        self.preferredStudents = 0
        self.major = majorContributedTo
        self.domain = domainCanBeTaughtIn
        self.needsAccessibility = False
    
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

class classInfo:
    def __init__(self, requiredProfessor, majorContributedTo, domainCanBeTaughtIn):
        self.professor = requiredProfessor
        self.major = majorContributedTo
        self.domain = domainCanBeTaughtIn

    def __str__(self):
        return f"prof: {self.professor} major: {self.major} domain {self.domain}"

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

class Room:
    def __init__(self, id, capacity, domain, accessible):
        self.id = id
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
        return f"{self.id} - {self.domain}"

# year3NonMajor1 = Student(1, 3, 1, 3) #id, class year, major preferredClassMajor
# year3NonMajor2 = Student(2, 3, 2, 3)
# year3Major = Student(3, 3, 3, 3)
# year2Major = Student(5, 2, 3, 3)
# year4NonMajor = Student(4, 2, 4, 3) #higher year

# print(f"year3Major > year2Major: {year3Major > year2Major}")
# print(f"year3Major < year2Major: {year3Major < year2Major}")
# print(f"year3Major == year2Major: {year3Major == year2Major}")
# print(f"year3Major != year2Major: {year3Major != year2Major}")
# print(f"year2Major > year4NonMajor: {year3Major > year2Major}")
# print(f"year2Major < year4NonMajor: {year3Major < year2Major}")
# print(f"year2Major == year4NonMajor: {year3Major == year2Major}")
# print(f"year2Major != year4NonMajor: {year3Major != year2Major}")
# print(f"year3NonMajor1 > year3NonMajor2: {year3NonMajor1 > year3NonMajor2}")
# print(f"year3NonMajor1 < year3NonMajor2: {year3NonMajor1 < year3NonMajor2}")
# print(f"year3NonMajor1 == year3NonMajor2: {year3NonMajor1 == year3NonMajor2}")
# print(f"year3NonMajor1 != year3NonMajor2: {year3NonMajor1 != year3NonMajor2}")

