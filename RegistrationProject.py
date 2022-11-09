import pandas as pd
import datetime
import DataStructures as ds
import sys

class Class:

    def __init__(self, class_name):
        self.name = class_name
        self.enrolled = []
        self.professor = -1
        self.time = -1
        self.room = -1
        self.preferredStudents = 0
    
    def notFull(self):
        return self.len(self.enrolled) - self.roomSize != 0

    def __str__(self):
        students = ""
        for s in self.enrolled:
            students += f"{s} "
        return f"{self.name}\t{self.room}\t{self.professor}\t{self.time}\t{students}"

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
    whoPrefers.append(ds.LinkedList()) #append blank -- no class 0

    for i in range(numClasses):
        mostPreferredClasses.append((0, i))
        whoPrefers.append(ds.LinkedList())

    file = open(studentsFilename)

    string = file.read()
    lines = string.split('\n')
    lines = lines[1:] #skip first line

    students = []
    students.append([]) #for 0 student
    i = 0
    # fill students
    for line in lines:
        i += 1
        if line == "":
            break
        
        line = line.split('\t')[1] #isolate student preferences
        pref = line.split(' ') #parse preferences

        if len(pref) == 0:
            break
        students.append([])
        students[i] = [int(p) for p in pref] #convert preferences to integers


    # for each class in each student preference list, increment that classes preference level
    i = -1
    whoPrefers.append(0) #0 prefer class 0 which doesn't exist --> I don't know what this does but I'm too scared to change it
    for student in students:
        i += 1
        for pref in student:
            mostPreferredClasses[pref-1] = (mostPreferredClasses[pref - 1][0] + 1, pref)
            whoPrefers[pref].append(i)

    # mergeSort the classes based on preference level

    # print(mostPreferredClasses)
    mergeSort(mostPreferredClasses, 1)
    # print(mostPreferredClasses)

    # turn mostPreferredClasses array from an array of tuples to a linked list of Class() objects
    #(will make O(1) removal/re-adding sections when conflicts)
    mostPreferred = ds.LinkedList()
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
    sched.append(ds.LinkedList()) #for 0 case class
    for i in range(size):
        sched.append(ds.LinkedList())
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

'''
    Given two classes, A and B, calculate how much student overlap they have. 
    Params: 
        classes, list of classes each with a list of students who wish to take that class 
            (whoPrefers[class], where class is a linked list)
    Returns: 
        ret, a 2D Array, where for each ret[i,j], it gives the percentage of students in class i
        who want to take class j
'''
def depart_conflicts(classes):
    # initialize the returned matrix
    ret = [[0 for i in range(len(classes))] for j in range(len(classes))]

    for i in range(len(classes)):
        classA = classes[i]
        for j in range(len(classes)):
            classB = classes[j]
            itt = classB.head
            while(itt != None):
                if classA.contains(itt.data):
                    ret[i][j] += 1
                itt = itt.next
            ret[i][j] = ret[i][j] / (classA.size)

    return ret

def classSchedule(constraints_filename, students_filename):
    #numTimeSlots - integer, number of time slots
    #rooms, unsorted linked list of rooms and associated sizes (size, room#)
    #classTeachers -- array of classes indexed by professor who teaches them
    numTimeSlots, maxRoomSize, classTeachers = parseConstraints(constraints_filename)
    mergeSort(maxRoomSize, 0)
    
    # initialize preferred students and Class ranked lists
    classRanks, studentPrefLists, whoPrefers = classQ(students_filename, len(classTeachers))
    classConflicts = depart_conflicts(whoPrefers)
    globalStudentCount = 0

    # innit student's schedules
    studentSchedules = generateSchedules(len(studentPrefLists))
    profSchedules = generateSchedules(int(len(classTeachers) / 2))

    holdClass = ds.LinkedList()
    schedule = []

    for room in maxRoomSize:
        schedule.append([])

    for room in maxRoomSize:
        for time in range(numTimeSlots):
            if classRanks.isEmpty():
                # df = pd.DataFrame(schedule)
                # df.columns = [f'time {t}' for t in range(numTimeSlots)]
                # df.index = [f'room {r[1]}' for r in maxRoomSize]
                # print(studentPreferenceCount)
                return schedule, globalStudentCount, globalStudentCount / (len(studentPrefLists) * 4)

            clss = classRanks.popFront().data

            skipTime = False
            skipRoom = False
            
            # checks every other class at our given time. there is a class where 75% of the students want to take that class, 
            # do not select the current class and move to the next class
            for r in maxRoomSize[0:room]:
                if(classConflicts[clss.name][schedule[r][time]] >= 0.75):
                    holdClass.append(clss)
                    skipRoom = True
                
                if classRanks.isEmpty():
                    skipTime = True
                    break

                clss = classRanks.popFront().data
            # if current professor has conflict, or the class conflicts with any class
            while profSchedules[classTeachers[clss.name]].contains(time) and not skipRoom:
                #while profSchedules[classFacts[clss.name].professor].contains(time):
                holdClass.append(clss)

                if classRanks.isEmpty():
                    skipTime = True
                    break

                clss = classRanks.popFront().data
            

            if skipTime == True:
                classRanks = holdClass
                continue

            if not holdClass.isEmpty():
                classRanks.merge(holdClass)

            clss.professor = classTeachers[clss.name]
            
            profSchedules[clss.professor].append(time)
            while not room[0] == len(clss.enrolled) and not whoPrefers[clss.name].isEmpty():
                x = whoPrefers[clss.name].popFront().data
                if(not studentSchedules[x].contains(time)):
                    clss.enrolled.append(x)
                    
                    studentSchedules[x].append(x) # TODO
                    globalStudentCount+=1

            clss.room = room[1]
            clss.time = time
            schedule[clss.room - 1].append(clss)
            # print(f"Room: {room[1]} - Class {clss.name}, prof {clss.professor}, time {time}")

    # df = pd.DataFrame(schedule)
    # df.columns = [f'time{t}' for t in range(numTimeSlots)]
    # df.index = [f'room {r[1]}' for r in maxRoomSize]
    return schedule, globalStudentCount, globalStudentCount / ((len(studentPrefLists) - 1) * 4)

file = open("output.txt", "w")
print(file)
file.write("Course\tRoom\tTeacher\tTime\tStudents\n")
user_consts_file = sys.argv[1]
user_prefs_file = sys.argv[2]
if(user_consts_file != None & user_prefs_file != None):
    schedule, globalStudentCount, score = classSchedule(user_consts_file, user_prefs_file)
else:
    schedule, globalStudentCount, score = classSchedule("demo_constraints.txt", "demo_studentprefs.txt")

for time in schedule:
    for clss in time:
        file.write(f"{clss}\n")

file.close()
