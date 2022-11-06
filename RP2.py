import pandas as pd
import datetime
import re
import DataStructures as ds
import classroomMechanics as mech

'''
parses contents of constraints.txt
params:
  file location of constraints.txt
returns: numTimeSlots, rooms, classFacts, domains
    numTimeSlots -- number of time slots (integer)
    rooms -- array of Room() objects - 
        Each Room() object in rooms holds the following pieces of information:
            id - the id of the room, integer
            capacity - the capacity of the room, integer
            domain - the domain in which the room is located, string
            accessible - whether or not the room is accessible, boolean
    classFacts -- array of classFacts() objects indexed by class id (size is number of classes)
        Each location in classFacts holds three pieces of information:
            classFacts[class_id].professor - the professor this class can be taught by
            classFacts[class_id].major - the major this class contributes to
            classFacts[class_id].domain - the domain this class must be taught in
    domains - an array of all domains
'''
def parseConstraints(filename):
    # open file, split by line
    file = open(filename)
    txt = file.read()
    txt = re.sub('[\n]+', '\n', txt)
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
        id = int(x[0])
        capacity = int(x[1])
        domain = x[2]
        accessible = True if int(x[3]) == 1 else False
        rooms.append(mech.Room(id, capacity, domain, accessible))
        loc += 1
    
    # split next line after rooms to get number of classes
    loc += 1
    x = lines[loc].split('\t')
    numClasses = int(x[1])
    
    # split next line to get number of class teachers.
    # we can discard this -- just half number of classes
    loc += 1
    x = lines[loc].split('\t')
    classTeachers = [] # array of classes indexed by classID (first is 0)
    classTeachers.append(0) #there is no 0 class

    domains = []
    # adding correct professor for each class
    for i in range(numClasses):
        loc += 1
        tc = lines[loc].split('\t')
        requiredProfessor = int(tc[1])
        majorContributedTo = int(tc[2])
        requiredDomain = tc[3]
        if domains.count(requiredDomain) == 0:
            domains.append(requiredDomain)
        classTeachers.append(mech.classInfo(requiredProfessor, majorContributedTo, requiredDomain))

    file.close() #close file
    return numTimeSlots, rooms, classTeachers, domains

'''
    generates an array of students
    @param studentsFilename = string filename of studentPreferenceList file
    @return an array of student tuplets -- each student[i] = (year, major, [class preferences])
'''   
def studentsArray(studentsFilename):
    file = open(studentsFilename)

    string = file.read()
    string = re.sub('[\n]+', '\n', string)
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
        
        line = re.sub('[\t]+', '\t', line)
        parts = line.split('\t') #parts now holds ['id', 'pref1 pref2 pref3 pref4 year major accomodations]
        line_pref = parts[1] #isolate student preferences
        year = int(parts[2])
        major = int(parts[3])
        accomodations = True if int(parts[4]) == 1 else False
        pref = line_pref.split(' ') #parse preferences


        if len(pref) == 0:
            break
        preferences_integers = [int(p) for p in pref] #convert preferences to integers
        students.append((i, year, major, preferences_integers))

    file.close()
    return students
# 
# params
#   FILE OBJECT of studentprefs.txt
#   number of classes as input
# returns
#   mostPreferred -- LinkedList of classes organized in descending order by how preferred they are
#   studentPreferences -- array of arrays. Outer array is indexed by student id, inner arrays are student preference lists
#   whoPrefers -- array of LinkedLists of students who prefer a class, indexed by class
def classQ(studentsFilename, numClasses):
    # array of tuples for merge sort reasons --> will turn into LinkedList() later
    # will be organized (preference level of class, class id)
    mostPreferredClasses = []

    studentPreferences = studentsArray(studentsFilename)

    #array of LinkedLists of all students who prefer class, indexed by class
    whoPrefers = []
    whoPrefers.append(ds.LinkedList()) #append blank -- no class 0

    for i in range(numClasses):
        mostPreferredClasses.append((0, i))
        whoPrefers.append(ds.LinkedList())
    
    # for each class in each student preference list, increment that classes preference level
    i = -1
    whoPrefers.append(ds.LinkedList()) #0 prefer class 0 which doesn't exist --> I don't know what this does and I'm too scared to change it
    for (id, year, major, preferences) in studentPreferences[1:]:
        i += 1
        for pref in preferences:
            whoPrefers[pref].append(mech.Student(id, year, major, pref)) #TODO use mech.Student() class to make sure sorting is correct

    #sort whoPrefers linked list in this order:
    for i in range(len(whoPrefers))[1:]:
        arr = whoPrefers[i].toArray()
        mergeSort(arr, 0)
        whoPrefers[i] = ds.arrayToLinkedList(arr)       

    # mergeSort the classes based on preference level
    mergeSort(mostPreferredClasses, 1)

    # turn mostPreferredClasses array from an array of tuples to a linked list of Class() objects
    #(will make O(1) removal/re-adding sections when conflicts)
    mostPreferred = ds.LinkedList()
    for (pref, id) in mostPreferredClasses:
        c = mech.Class(id)
        c.preferredStudents = pref
        mostPreferred.append(c)

    return mostPreferred, studentPreferences, whoPrefers

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
 
def classSchedule(constraints_filename, students_filename):
    #numTimeSlots - integer, number of time slots
    #rooms, unsorted linked list of rooms and associated sizes (size, room#)
    #classFacts -- array of classes indexed by id and their associated facts
        #each location contains:
        #classFacts[class_id].professor - professor required to teach class_id
        #classFacts[class_id].major - major class_id contributes to
        #classFacts[class_id].domain - domain class_id must be taught in
    #domains - array of all domains TODO: do something with the domains -- possible list of maxRoomSizes for all domains?                                   
    numTimeSlots, maxRoomSize, classFacts, domains = parseConstraints(constraints_filename)
    mergeSort(maxRoomSize, 0)
    
    # initialize preferred students and Class ranked lists
    classRanks, studentPrefLists, whoPrefers = classQ(students_filename, len(classFacts))
    globalStudentCount = 0

    # innit student's schedules
    studentSchedules = generateSchedules(len(studentPrefLists))
    profSchedules = generateSchedules(int(len(classFacts) / 2))

    holdClass = ds.LinkedList()
    schedule = []

    for room in maxRoomSize:
        schedule.append([])

    for room in maxRoomSize:
        for time in range(numTimeSlots):
            if classRanks.isEmpty():
                return schedule, globalStudentCount, globalStudentCount / ((len(studentPrefLists) - 1) * 4)

            clss = classRanks.popFront().data

            skipTime = False
            if clss.name == 0:
                continue

            while profSchedules[classFacts[clss.name].professor].contains(time):
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

            clss.professor = classFacts[clss.name].professor
            
            profSchedules[clss.professor].append(time)
            while not room.capacity == len(clss.enrolled) and not whoPrefers[clss.name].isEmpty():
                x = whoPrefers[clss.name].popFront().data.id #student id
                if(not studentSchedules[x].contains(time)):
                    clss.enrolled.append(x)
                    
                    studentSchedules[x].append(x)
                    globalStudentCount+=1

            clss.room = room.id
            clss.time = time
            schedule[clss.room - 1].append(clss)
            

    return schedule, globalStudentCount, globalStudentCount / ((len(studentPrefLists) - 1) * 4)

mostPreferred, studentPreferences, whoPrefers = classQ("mod_studentprefs_demo.txt", 14)
numTimeSlots, rooms, classFacts, domains = parseConstraints("mod_constraints_demo.txt")

file = open("../basic/output.txt", "w")
file.write("Course\tRoom\tTeacher\tTime\tStudents\n")
schedule, globalStudentCount, score = classSchedule("mod_constraints_demo.txt", "mod_studentprefs_demo.txt")

for time in schedule:
    for clss in time:
        file.write(f"{clss}\n")