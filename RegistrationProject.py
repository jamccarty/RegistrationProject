import re
from re import S, X

class LinkedList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self):
        self.head = None

    def __str__(self) -> str:
        s = ""
        loc = self.head

        while loc != None:
            s += f" -> {loc.data}"
            loc = loc.next
        
        return s

    def append(self, data):
        n = self.Node(data)

        if self.head == None:
            self.head = n
        else:
            n.next = self.head
            self.head = n

    def popFront(self):
        n = self.head
        self.head = n.next
        return n
    def isEmpty(self):
        return self.head.next is None

class Class:
    def __init__(self, class_name):
        self.name = class_name
        self.enrolled = []
        self.professor = -1
        self.time = -1
        self.preferredStudents = 0

    def __str__(self):
        return f"{self.name}"

# parses contents of constraints.txt
# params:
#   file location 
# returns 
#   number of time slots (integer)
#   rooms (array of 2-tuples (roomsize, room number)), 
#   array of professors indexed by class they teach (size is number of classes)
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
def classQ(studentPrefsFile, numClasses):
    # array of tuples for merge sort reasons --> will turn into LinkedList() later
    # will be organized (preference level of class, class id)
    mostPreferredClasses = []

    for i in range(numClasses):
        mostPreferredClasses.append((0, i))

    string = studentPrefsFile.read()
    lines = string.split('\n')
    lines = lines[1:] #skip first line

    students = []

    # fill students
    for line in lines:
        line = re.sub('[ \t]+', ' ', line)
        pref = line.split(' ')[1:]
        prefno = [int(p) for p in pref]
        students.append(prefno)

    # for each class in each student preference list, increment that classes preference level
    for student in students:
        for pref in student:
            mostPreferredClasses[pref-1] = (mostPreferredClasses[pref - 1][0] + 1, pref)

    # mergeSort the classes based on preference level
    mergeSort(mostPreferredClasses, 1)

    # turn mostPreferredClasses array from an array of tuples to a linked list of Class() objects
    #(will make O(1) removal/re-adding sections when conflicts)
    mostPreferred = LinkedList()
    for (pref, id) in mostPreferredClasses:
        c = Class(id)
        c.preferredStudents = pref
        mostPreferred.append(c)

    return mostPreferred, students

def roomQ(rooms):
    # input: list of rooms - [size, room #] (tuple)
    sorted_rooms = mergeSort(rooms, 0)
    ret_list = LinkedList()

    for i in range(len(sorted_rooms)):
        ret_list.append(sorted_rooms[i])

    return ret_list

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
 
def classSchedule(filename, students_filename):
    # parse contents to get time slots, rooms, and professors
    timeslots, rooms, classProf = parseConstraints(filename)
    # initialize preferred students and class ranked lists
    classRanks, studentPref = classQ(students_filename, classes) 
    #initialize the list of rooms
    maxRoomSize = roomQ(rooms)
    globalStudentCount = 0

    # innit professors 
    profSchedule = []
    for i in range(len(classProf)):
        profSchedule.append([])

    # innit student's schedules
    studentSchedules = []
    for i in range(len(studentPref)):
        studentSchedules.append([])

    holdClass = []
    for room in maxRoomSize:
        for time in timeslots:
            if classRanks.isEmpty():
                return globalStudentCount
            clss = classRanks.popFront()
            while classProf[clss].conflicts(timeslots):
                holdClass.append(clss)
                clss = classRanks.popFront()
            for item in holdClass:
                classRanks.append(item)
            prof = classProf[clss]
            # TODO: make studentPref into a LinkedList and clss.notFull thing
            prof.schedule.append(time) #TODO 
            while(clss.notFull and (studentPref.isEmpty())):
                x = studentPref.popFront()
                if(not x.timeConflict):
                    studentSchedules[].append(x) # TODO
                    globalStudentCount+=1
            studentPreferenceCount = globalStudentCount / 4
            print(studentPreferenceCount)
# Code to print the list
def printList(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()
 
 
# Driver Code
if __name__ == '__main__':
    arr = [12, 11, 13, 5, 6, 7]
    print("Given array is", end="\n")
    printList(arr)
    mergeSort(arr,1)
    print("Sorted array is: ", end="\n")
    printList(arr)

stud = open("demo_studentprefs.txt")
li, s = classQ(stud, 14)

times, rooms, classes, teachers = parseConstraints("../basic/demo_constraints.txt")
print(f"class times: {times}")
print(f"rooms: {rooms}")
print(f"number of classes: {classes}")
print(f"teachers list: {teachers}")


