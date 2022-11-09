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

    domains = []
    dom_id = 0 #id for next added domain() in domains array, starts at 0
    domainIndexDict = {}
    classes = []

    # initialize rooms array -- array of tuples (room size, room id)
    # (this is so that after merge sorting, each size remains paired with correct room id)
    for line in lines[2:2 + numRooms]:
        x = line.split('\t')
        id = int(x[0])
        capacity = int(x[1])
        domain = mech.domain(x[2], dom_id)
        inDomains = False

        for d in domains:
            if d == domain:
                inDomains = True

        if not inDomains:
            domains.append(domain)
            classes.append([])
            domainIndexDict.update({x[2]:dom_id})
            dom_id += 1

        accessible = True if int(x[3]) == 1 else False
        domain.id = domainIndexDict[domain.name]
        rooms.append(mech.Room(id, capacity, domain, accessible))
        loc += 1
    
    # split next line after rooms to get number of classes
    loc += 1
    x = lines[loc].split('\t')
    numClasses = int(x[1])


    for i in range(len(classes)):
        classes[i].append(None) #for 0 class, which does not exist
        for c in range(numClasses):
            classes[i].append(None)
    
    # split next line to get number of class teachers.
    # we can discard this -- just half number of classes
    loc += 1
    x = lines[loc].split('\t')
    # classTeachers = [] # array of classes indexed by classID (first is 0)
    # classTeachers.append(0) #there is no 0 class

    # adding correct professor for each class
    for i in range(numClasses):
        loc += 1
        tc = lines[loc].split('\t')
        requiredProfessor = int(tc[1])
        majorContributedTo = int(tc[2])
        requiredDomain = mech.domain(tc[3], domainIndexDict[tc[3]])
        isEsem = True if int(tc[4]) == 1 else False
        classes[requiredDomain.id][i+1] = mech.Class(i+1, requiredProfessor, majorContributedTo, requiredDomain, isEsem)

    file.close() #close file
    return numTimeSlots, rooms, classes, numClasses

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
        students.append((i, year, major, preferences_integers, accomodations))

    file.close()
    return students

def accessibleSchedule(schedule, rooms, numTimes, access_classes, access_esems, whoPrefers, student_schedules, prof_schedules):
    access_rooms = []

    for r in rooms:
        if r.accessible == True:
            access_rooms.append(r)

    mergeSort(access_rooms, 1)

    taken_time_room_combos = []

    for r in access_rooms:
        domain = r.domain.id
        for c in access_esems[domain]:
            if c.preferredStudents <= r.capacity and not prof_schedules[c.professor].contains(t):
                schedule[r.id][0] = c
                c.time = 0
                c.room = r
                while not whoPrefers[c.name].isEmpty():
                    student = whoPrefers[c.name].popFront()
                    c.enrolled.append(student)
                    student_schedules[student.id].append(0)
                    taken_time_room_combos.append((0, r.id))

    for r in access_rooms:
        domain = r.domain.id
        for t in range(numTimes)[1:]:
            for c in access_classes[domain]:
                if c.preferredStudents <= r.capacity and not prof_schedules[c.professor].contains(t):
                    schedule[r.id][t] = c
                    c.time = 0
                    c.room = r
                    while not whoPrefers[c.name].isEmpty():
                        student = whoPrefers[c.name].popFront()
                        if not student_schedules[student.id].contains(t):
                            c.enrolled.append(student)
                            student_schedules[student.id].append(0)
                            taken_time_room_combos.append((t, r.id))
                else:
                    break

    return taken_time_room_combos


# 
# modifies classes to be an array of LinkedList() objects, where each class[domain.id] = LinkedList() of classes
# to be taught in that domain
# params
#   FILE OBJECT of studentprefs.txt
#   number of classes as input
# returns
#   studentPreferences -- array of arrays. Outer array is indexed by student id, inner arrays are student preference lists
#   whoPrefers -- array of LinkedLists of students who prefer a class, indexed by class
def classQ(studentsFilename, classes, numClasses):
    studentPreferences = studentsArray(studentsFilename)

    #array of LinkedLists of all students who prefer class, indexed by class
    whoPrefers = []
    whoPrefers.append(ds.LinkedList()) #append blank -- no class 0
    tempClasses = [] #temporary array of all classes -- will be discarded with stack frame

    esems = []

    access_esems = [] #esems that need to be accessible, indexed by domain
    access_classes = [] #classes that need to be accessible, indexed by domain

    for d in range(len(classes)): #for number of domains
        esems.append([])
        esems[d].append(None) #0 class does not exist

        access_esems.append([]) #don't need to be indexed
        access_classes.append([]) #don't need to be indexed

        for c in range(numClasses): #for each class
            esems[d].append(None)

    for domain in classes:
        for clss in domain:
            if not clss is None:
                whoPrefers.append(ds.LinkedList())
                tempClasses.append(clss)
    # for each class in each student preference list, increment that classes preference level
    i = -1
    whoPrefers.append(ds.LinkedList()) #0 prefer class 0 which doesn't exist --> I don't know what this does and I'm too scared to change it
    print(len(whoPrefers))
    for (id, year, major, preferences, accomodations) in studentPreferences[1:]:
        i += 1
        for pref in preferences:
            print(pref)
            whoPrefers[pref].append(mech.Student(id, year, major, pref, accomodations))
            if accomodations == True:
                d = tempClasses[pref].domain.id
                # tempClasses[pref].needsAccessibility = True
                if tempClasses[pref].isEsem == True:
                    access_esems[d].append(tempClasses[pref])
                else:
                    access_classes[d].append(tempClasses[pref])
                tempClasses[pref] = None #no longer in tempClasses list -- in classes that need accessibility

    for clss in tempClasses:
        if not clss is None:
            if clss.isEsem == True:
                esems[clss.domain.id][clss.name] = clss
                esems[clss.domain.id][clss.name].preferredStudents = whoPrefers[clss.name].size
                # esems[clss.domain.id][clss.name].needsAccessibility = clss.needsAccessibility

                classes[clss.domain.id][clss.name] = None


            else:
                classes[clss.domain.id][clss.name].preferredStudents = whoPrefers[clss.name].size
                # classes[clss.domain.id][clss.name].needsAccessibility = clss.needsAccessibility

    #sort each whoPrefers[class] linked list in this order: majorSenior > majorJunior > nonMajorSenior > nonMajorJunior > Soph > Fresh
    for i in range(len(whoPrefers))[1:]:
        arr = whoPrefers[i].toArray()
        mergeSort(arr, 0)
        whoPrefers[i] = ds.arrayToLinkedList(arr)      

    for i in range(len(classes)):
        classes[i] = ds.removeBlanks(classes[i])
        mergeSort(classes[i], 0)
        classes[i] = ds.arrayToLinkedList(classes[i])

        esems[i] = ds.removeBlanks(esems[i])
        mergeSort(esems[i], 0)
        esems[i] = ds.arrayToLinkedList(esems[i])

        mergeSort(access_esems[i], 1)
        mergeSort(access_classes[i], 1)

    return studentPreferences, whoPrefers, esems, access_classes, access_esems

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
    numTimeSlots, maxRoomSize, classes, numClasses = parseConstraints(constraints_filename)
    mergeSort(maxRoomSize, 0)
    
    # initialize preferred students and Class ranked lists
    studentPrefLists, whoPrefers, esems, access_classes, access_esems = classQ(students_filename, classes, numClasses)
    globalStudentCount = 0

    # innit student's schedules
    studentSchedules = generateSchedules(len(studentPrefLists))
    profSchedules = generateSchedules(int(numClasses / 2))

    holdClass = ds.LinkedList()
    schedule = []

    for r in range(len(maxRoomSize)):
        schedule.append([])
        for t in range(numTimeSlots):
            schedule[r].append(None) 

    taken_time_room_combos = accessibleSchedule(schedule, maxRoomSize, numTimeSlots, access_classes, access_esems, whoPrefers, studentSchedules, profSchedules)

    for room in maxRoomSize:
        for time in range(numTimeSlots):
            if (time, room.id) in taken_time_room_combos:
                continue
            if classes[room.domain.id].isEmpty():
                return schedule, globalStudentCount, globalStudentCount / ((len(studentPrefLists) - 1) * 4)

            if not esems[room.domain.id].isEmpty() and time == 0:
                clss = esems[room.domain.id].popFront()
            else:
                clss = classes[room.domain.id].popFront()

            skipTime = False
            if clss.name == 0:
                continue

            while profSchedules[clss.professor].contains(time):
                holdClass.append(clss)

                if classes[room.domain.id].isEmpty():
                    skipTime = True
                    break

                clss = classes[room.domain.id].popFront()

            if skipTime == True:
                classes[room.domain.id] = holdClass
                continue

            if not holdClass.isEmpty():
                classes[room.domain.id].merge(holdClass)
            
            profSchedules[clss.professor].append(time)
            while not room.capacity == len(clss.enrolled) and not whoPrefers[clss.name].isEmpty():
                x = whoPrefers[clss.name].popFront().id #student id
                if(not studentSchedules[x].contains(time)):
                    clss.enrolled.append(x)
                    
                    studentSchedules[x].append(x)
                    globalStudentCount+=1

            clss.room = room.id
            clss.time = time
            schedule[clss.room - 1][time] = clss

    return schedule, globalStudentCount, globalStudentCount / ((len(studentPrefLists) - 1) * 4)

# numTimeSlots, maxRoomSize, classes, domains = parseConstraints("scripts/esemtinyc.txt")
# studentPreferences, whoPrefers = classQ("scripts/esemtinyp.txt", classes)

file = open("mod_output.txt", "w")
file.write("Course\tRoom\tTeacher\tTime\tStudents\n")
schedule, globalStudentCount, score = classSchedule("scripts/testB/constraints_0", "scripts/testB/prefs_0")

for time in schedule:
    for clss in time:
        if not clss is None:
            file.write(f"{clss}\n")

print(score)