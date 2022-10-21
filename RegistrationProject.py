from email import header
import re
from re import S, X

class LinkedList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None

    def __init__(self):
        self.head = None
        self.tail = None

    def __str__(self) -> str:
        s = ""
        loc = self.head

        while loc != None:
            s += f" -> {loc.data}"
            loc = loc.next
        
        return s

    def prepend(self, data):
        n = self.Node(data)

        if self.head == None:
            self.head = n
            self.tail = n
        else:
            n.next = self.head
            self.head.prev = n
            self.head = n
    
    def append(self, data):
        n = self.Node(data)

        if self.tail == None:
            self.head = n
            self.tail = n
        else:
            self.tail.next = n
            n.prev = self.tail
            self.tail = n

    def popFront(self):
        if self.head == None:
            return None
        if self.head.next == None:
            n = self.head
            self.head = None
            return n
        
        n = self.head

        if not n.next == None:
            self.head = n.next
        return n
    
    # merge two linked lists so that A->B
    def merge(self, A):
        self.tail.next = A.head
        A.head.prev = self.tail
        A.head = None
        self.tail = A.tail

    def contains(self, data):
        loc = self.head

        while loc != None:
            if loc.data == data:
                return True
            loc = loc.next
        
        return False

    def isEmpty(self):
        return self.head == None

class Class:

    def __init__(self, class_name):
        self.name = class_name
        self.enrolled = []
        self.professor = -1
        self.time = -1
        self.room = -1
        self.roomSize = 0
        self.preferredStudents = 0
    
    def notFull(self):
        return self.len(self.enrolled) - self.roomSize != 0

    def __str__(self):
        return f"{self.name}"

# parses contents of constraints.txt
# params:
#   file location 
# returns 
#   numTimeSlots -- number of time slots (integer)
#   rooms -- array of 2-tuples (roomsize, room number)), 
#   classTeachers -- array of professors indexed by class they teach (size is number of classes)
def parseConstraints(filename):
    # open file, split by line
    file = open(filename)
    txt = file.read()
    lines = txt.split('\n')

    # loc is current line number in file. tracks location in file
    loc = 0

    # x will hold parsed, string contents of file. 
    # variable names are always separated from values by \t
    x = lines[loc].split('\t')
    numTimeSlots = int(x[1]) # first line is number of time slots

    # parse next line
    loc += 1
    x = lines[loc].split('\t')
    numRooms = int(x[1]) #number of rooms total
    rooms = []

    # initialize rooms array -- array of tuples (room size, room id)
    # (this is so that after merge sorting, each size remains paired with correct room id)
    for line in lines[2:2 + numRooms]:
        x = line.split('\t')
        rooms.append((int(x[1]), int(x[0])))
        loc += 1
    
    # split next line after rooms to get number of classes
    loc += 1
    x = lines[loc].split('\t')
    numClasses = int(x[1])
    
    # split next line to get number of class teachers.
    # we can discard this -- just half number of classes
    loc += 1
    x = lines[loc].split('\t')
    classTeachers = [] # array of classes indexed by professor (first is 0)
    classTeachers.append(0) #there is no 0 class

    # adding correct professor for each class
    for i in range(numClasses):
        loc += 1
        tc = lines[loc].split('\t')
        classTeachers.append(int(tc[1]))

    file.close() #close file
    return numTimeSlots, rooms, classTeachers
    
# 
# params
#   FILE OBJECT of studentprefs.txt
#   number of classes as input
# returns
#   mostPreferred -- LinkedList of classes organized in descending order by how preferred they are
#   students -- array of arrays. Outer array is indexed by student id, inner arrays are student preference lists
#   whoPrefers -- array of LinkedLists of students who prefer a class, indexed by class
def classQ(studentsFilename, numClasses):
    # array of tuples for merge sort reasons --> will turn into LinkedList() later
    # will be organized (preference level of class, class id)
    mostPreferredClasses = []

    #array of LinkedLists of all students who prefer class, indexed by class
    whoPrefers = []
    whoPrefers.append(LinkedList()) #append blank -- no class 0

    for i in range(numClasses):
        mostPreferredClasses.append((0, i))
        whoPrefers.append(LinkedList())

    file = open(studentsFilename)

    string = file.read()
    lines = string.split('\n')
    lines = lines[1:] #skip first line

    students = []
    students.append([]) #for 0 student
    i = 0
    # fill students
    for line in lines:
        if line == "":
            break
        students.append([])
        line = line.split('\t')[1] #isolate student preferences
        pref = line.split(' ') #parse preferences
        students[i] = [int(p) for p in pref] #convert preferences to integers
        i += 1

    # for each class in each student preference list, increment that classes preference level
    i = -1
    for student in students:
        i += 1
        for pref in student:
            mostPreferredClasses[pref-1] = (mostPreferredClasses[pref - 1][0] + 1, pref)
            whoPrefers[pref - 1].append(i)

    # mergeSort the classes based on preference level
    print(mostPreferredClasses)
    mergeSort(mostPreferredClasses, 1)
    print(mostPreferredClasses)

    # turn mostPreferredClasses array from an array of tuples to a linked list of Class() objects
    #(will make O(1) removal/re-adding sections when conflicts)
    mostPreferred = LinkedList()
    for (pref, id) in mostPreferredClasses:
        c = Class(id)
        c.preferredStudents = pref
        mostPreferred.append(c)

    file.close()
    return mostPreferred, students, whoPrefers

'''
    generates array of LinkedList, where each LinkedList can hold time slots [person_index] has a class
    
    Params: 
        size -- number of people in array (ex: number of professors)
    Return:
        sched -- array of LinkedLists
    
'''
def generateSchedules(size):
    sched = []
    sched.append(LinkedList()) #for 0 case class
    for i in range(size):
        sched.append(LinkedList())
    return sched

#0 is greatest -> least, 1 is least -> greatest
def mergeSort(arr, dir):
    if len(arr) > 1:
 
         # Finding the mid of the array
        mid = len(arr)//2
 
        # Dividing the array elements
        L = arr[:mid]
 
        # into 2 halves
        R = arr[mid:]
 
        # Sorting the first half
        mergeSort(L, dir)
 
        # Sorting the second half
        mergeSort(R, dir)
 
        i = j = k = 0
 
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if(dir==0):
                if L[i] > R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
            elif(dir==1):
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
            k += 1
 
        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
 
def classSchedule(constraints_filename, students_filename):
    #numTimeSlots - integer, number of time slots
    #rooms, unsorted linked list of rooms and associated sizes (size, room#)
    #classTeachers -- array of classes indexed by professor who teaches them
    numTimeSlots, maxRoomSize, classTeachers = parseConstraints(constraints_filename)
    mergeSort(maxRoomSize, 0)
    print(maxRoomSize)
    
    # initialize preferred students and Class ranked lists
    classRanks, studentPrefLists, whoPrefers = classQ(students_filename, len(classTeachers))
    globalStudentCount = 0

    # innit student's schedules
    studentSchedules = generateSchedules(len(studentPrefLists))
    profSchedules = generateSchedules(int(len(classTeachers) / 2))
    print(len(profSchedules))

    holdClass = LinkedList()
    schedule = []
    for room in maxRoomSize:
        schedule.append([])
        for time in range(numTimeSlots):
            if classRanks.isEmpty():
                return schedule, globalStudentCount

            clss = classRanks.popFront().data

            skipTime = False
            while profSchedules[classTeachers[clss.name]].contains(time):
                # print(f"Conflict: {clss.name} at time {time}")
                holdClass.append(clss)
                clss = classRanks.popFront().data

                if classRanks.isEmpty():
                    skipTime = True
                    break

            if skipTime == True:
                classRanks = holdClass
                continue

            if not holdClass.isEmpty():
                classRanks.merge(holdClass)

            clss.professor = classTeachers[clss.name]

            # TODO: make studentPref into a LinkedList and clss.notFull thing
            profSchedules[clss.professor].append(time)
            while not room[0] == len(clss.enrolled) and not whoPrefers[clss.name].isEmpty():
                x = whoPrefers[clss.name].popFront().data
                if(not studentSchedules[x].contains(time)):
                    clss.enrolled.append(x)
                    studentSchedules[x].append(x) # TODO
                    globalStudentCount+=1

            print(f"Room: {room[1]} - Class {clss.name}, prof {clss.professor}, time {time}")
                

    studentPreferenceCount = globalStudentCount / 4
    print(studentPreferenceCount)

# # Code to print the list
# def printList(arr):
#     for i in range(len(arr)):
#         print(arr[i], end=" ")
#     print()
 
 
# # Driver Code
# if __name__ == '__main__':
#     arr = [12, 11, 13, 5, 6, 7]
#     print("Given array is", end="\n")
#     printList(arr)
#     mergeSort(arr,1)
#     print("Sorted array is: ", end="\n")
#     printList(arr)

constraints = "../basic/demo_constraints.txt"
studprefs = "../basic/demo_studentprefs.txt"

classSchedule(constraints, studprefs)
# li, s, x = classQ("demo_studentprefs.txt", 14)

# times, rooms, classTeachers = parseConstraints("../basic/demo_constraints.txt")
# print(f"class times: {times}")
# print(f"rooms: {rooms}")
# print(f"number of classes: {classTeachers}")


