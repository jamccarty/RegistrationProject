import pandas as pd
import datetime
import re
import DataStructures as ds
import classroomMechanics as mech
import sys


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

def accessibleSchedule(schedule, rooms, numTimes, globalStudentCount, access_classes, access_esems, whoPrefers, student_schedules, prof_schedules, notAddedDict):
    access_rooms = []
    for i in range(len(access_classes)):
        access_classes[i] = ds.arrayToLinkedList(access_classes[i])

    for r in rooms:
        if r.accessible == True:
            access_rooms.append(r)

    mergeSort(access_rooms, 1)

    taken_time_room_combos = []

    for r in access_rooms:
        domain = r.domain.id
        for c in access_esems[domain]:
            if c.preferredStudents <= r.capacity and not prof_schedules[c.professor].contains(0):
                if c.name in notAddedDict:
                    notAddedDict.pop(c.name)
                schedule[r.id - 1][0] = c
                c.time = 0
                c.room = r
                for x in whoPrefers[c.name]:
                    # print(x)
                    student = x.id
                    c.enrolled.append(student)
                    student_schedules[student].append(0)
                    taken_time_room_combos.append((0, r.id))
            else:
                notAddedDict.update({c.name:'not enough accessible rooms'})
    if(len(access_rooms) == 0):
        for domain in range(len(access_classes)):
            for c in access_esems[domain]:
                notAddedDict.update({c.name: 'not enough accessible rooms'})
            while not access_classes[domain].isEmpty():
                c = access_classes[domain].popFront()
                notAddedDict.update({c.name: 'not enough accessible rooms'})

    schedule, globalStudentCount = miniSchedule(schedule, access_classes, access_rooms, range(numTimes)[1:], 
                                                globalStudentCount, student_schedules, prof_schedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict)

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
    whoPrefers.append([]) #append blank -- no class 0
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

    tempClasses.append(None) #0 class does not exist
    for domain in classes:
        for clss in domain:
            if not clss is None:
                whoPrefers.append([])
                tempClasses.append(None)
    for domain in classes:
        for clss in domain:
            if not clss is None:
                tempClasses[clss.name] = clss

    # for each class in each student preference list, increment that classes preference level
    i = -1
    whoPrefers.append([]) #0 prefer class 0 which doesn't exist --> I don't know what this does and I'm too scared to change it
    for (id, year, major, preferences, accomodations) in studentPreferences[1:]:
        i += 1
        for pref in preferences:
            whoPrefers[pref].append(mech.Student(id, year, major, pref, accomodations))
            if accomodations == True and not tempClasses[pref] is None:
                d = tempClasses[pref].domain.id
                # tempClasses[pref].needsAccessibility = True
                if tempClasses[pref].isEsem == True:
                    access_esems[d].append(tempClasses[pref])
                    esems[d][pref] = None
                else:
                    access_classes[d].append(tempClasses[pref])
                    classes[d][pref] = None
                tempClasses[pref] = None #no longer in tempClasses list -- in classes that need accessibility
    count = 0
    for clss in tempClasses:
        count += 1
        if not clss is None:
            if clss.isEsem == True:
                esems[clss.domain.id][clss.name] = clss
                esems[clss.domain.id][clss.name].preferredStudents = len(whoPrefers[clss.name])
                # esems[clss.domain.id][clss.name].needsAccessibility = clss.needsAccessibility

                classes[clss.domain.id][clss.name] = None


            else:
                classes[clss.domain.id][clss.name].preferredStudents = len(whoPrefers[clss.name])
                # classes[clss.domain.id][clss.name].needsAccessibility = clss.needsAccessibility

    #sort each whoPrefers[class] linked list in this order: majorSenior > majorJunior > nonMajorSenior > nonMajorJunior > Soph > Fresh
    for i in range(len(whoPrefers))[1:]:
        mergeSort(whoPrefers[i], 0)   

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
 

def miniSchedule(schedule, classes, maxRoomSize, timeSlots, globalStudentCount, studentSchedules, profSchedules, whoPrefers, taken_time_room_combos, notAddedDict):
    holdClass = ds.LinkedList()
    
    for room in maxRoomSize:
        for time in timeSlots:
            if (time, room.id) in taken_time_room_combos:
                print(f"({time}, {room}) taken")
                continue
            if classes[room.domain.id].isEmpty():
                return schedule, globalStudentCount

            clss = classes[room.domain.id].popFront()

            skipTime = False
            if clss.name == 0:
                continue
            infiniteLoopOption = False
            while profSchedules[clss.professor].contains(time):
                if classes[room.domain.id].isEmpty():
                    infiniteLoopOption = True
                holdClass.append(clss)

                if infiniteLoopOption == True:
                    classes[room.domain.id].head = None
                    classes[room.domain.id].head = None

                notAddedDict.update({clss.name : 'professor schedule conflict'})

                if classes[room.domain.id].isEmpty():
                    skipTime = True
                    break
            
                clss = classes[room.domain.id].popFront()

            if skipTime == True:
                classes[room.domain.id] = holdClass
                continue
            
            if clss.name in notAddedDict:
                notAddedDict.pop(clss.name)

            if not holdClass.isEmpty():
                classes[room.domain.id].merge(holdClass)
            
            profSchedules[clss.professor].append(time)
            for student in whoPrefers[clss.name]:
                x = student.id
                if len(clss.enrolled) == room.capacity:
                    break
                if(not studentSchedules[x].contains(time)):
                    clss.enrolled.append(x)
                    
                    studentSchedules[x].append(time)
                    globalStudentCount+=1

            clss.room = room
            clss.time = time
            schedule[clss.room.id - 1][time] = clss
        for r in maxRoomSize[:room.id]:
            conflictSchedule(schedule[r.id - 1], whoPrefers, studentSchedules, profSchedules, globalStudentCount)

    return schedule, globalStudentCount

def conflictSchedule(room_schedule, whoPrefers, studentSchedules, profSchedules, globalStudentCount):
    for time in range(len(room_schedule[1:])): #non esems
        currClass = room_schedule[time]
        orgStu = []
        maxSwpStu = ([], [])
        maxSwpLen = -1
        maxSwpIndex = -1

        if currClass is None:
            continue

        room = currClass.room

        for t2 in range(len(room_schedule[1:time])): #no esems
            swapClass = room_schedule[t2] #class currClass would be swapping spots with
            swpStu = [] #students that would be enrolled in the swapClass at time t2
            if swapClass is None: #if t2 has a class scheduled
                continue #TODO we should still probably check to see if swapping currClass to this time would increase the number of enrolled students
            if profSchedules[swapClass.professor].contains(time):
                continue

            #tally number of students who would be enrolled in swapClass if swapClass was scheduled at time
            for student in whoPrefers[swapClass.name]:
                x = student.id
                if not studentSchedules[x].contains(time):
                    swpStu.append(x)
                if len(swpStu) > room.capacity:
                    break
            #tallying number of students who would be enrolled in currClass if currClass was scheduled at t2
            for student in whoPrefers[currClass.name]:
                x = student.id
                if not studentSchedules[x].contains(t2):
                    orgStu.append(x)
                if len(orgStu) > room.capacity:
                    break
            
            #if the number of total students enrolled would be greater if swapClass and currClass swapped times,
            #set maxSwpLen = swpLen
            if len(currClass.enrolled) + len(swapClass.enrolled) < len(swpStu) + len(orgStu):
                for student in whoPrefers[currClass.name]:
                    x = student.id
                    if studentSchedules[x].contains(t2):
                        orgStu.append(x)
                swpLen = len(orgStu) + len(swpStu)
                orgLen = len(currClass.enrolled) + len(swapClass.enrolled)
                if swpLen > orgLen: #TODO we should also probably have some sort of maxOrgLen and maxOrgStu array as well, since we've already calculated them
                    if swpLen > maxSwpLen:
                        maxSwpLen = swpLen
                        maxSwpStu = (orgStu, swpStu)
                        maxSwpIndex = t2
                
        if maxSwpIndex != -1:
            #print(f"org enrollment: {len(room_schedule[time].enrolled)} + {len(room_schedule[maxSwpIndex].enrolled)} -> {len(maxSwpStu[0])} + {len(maxSwpStu[1])}")
            globalStudentCount -= len(room_schedule[time].enrolled)
            globalStudentCount -= len(room_schedule[maxSwpIndex].enrolled)

            room_schedule[time].enrolled = maxSwpStu[0]
            room_schedule[maxSwpIndex].enrolled = maxSwpStu[1]


            for student in room_schedule[time].enrolled:
                studentSchedules[student].remove(time)
                studentSchedules[student].append(maxSwpIndex)
            for student in room_schedule[maxSwpIndex].enrolled:
                studentSchedules[student].remove(maxSwpIndex)
                studentSchedules[student].append(time)
            room_schedule[time], room_schedule[maxSwpIndex] = room_schedule[maxSwpIndex], room_schedule[time]
            globalStudentCount += len(room_schedule[time].enrolled) + len(room_schedule[maxSwpIndex].enrolled)


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

    schedule = []

    for r in range(len(maxRoomSize)):
        schedule.append([])
        for t in range(numTimeSlots):
            schedule[r].append(None) 

    notAddedDict = {} #dictionary of reasons for why each unadded class went unadded
    taken_time_room_combos = accessibleSchedule(schedule, maxRoomSize, numTimeSlots, globalStudentCount,
                                                access_classes, access_esems, whoPrefers, 
                                                studentSchedules, profSchedules, notAddedDict)

    #schedule esems for 0 time slot
    schedule, globalStudentCount = miniSchedule(schedule, esems, maxRoomSize, [0], 
                                                globalStudentCount, studentSchedules, profSchedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict)

    #0 non-accomodations classes for all other time slots
    schedule, globalStudentCount = miniSchedule(schedule, classes, maxRoomSize, range(numTimeSlots)[1:],
                                                globalStudentCount, studentSchedules, profSchedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict)

    return schedule, globalStudentCount, globalStudentCount / ((len(studentPrefLists) - 1) * 4), notAddedDict

#numTimeSlots, maxRoomSize, classes, domains = parseConstraints("scripts/esemtinyc.txt")
# studentPreferences, whoPrefers = classQ("scripts/esemtinyp.txt", classes)

user_consts_file = "testE/constraints_0"
user_prefs_file =  "testE/prefs_0"
if len(sys.argv) >= 2:
    user_consts_file = sys.argv[1]
    user_prefs_file = sys.argv[2]

start = datetime.datetime.now().microsecond / 1000.0
schedule, globalStudentCount, score, notAddedDict = classSchedule(user_consts_file, user_prefs_file)
end = datetime.datetime.now().microsecond / 1000.0
print(f"start: {start} end: {end} time taken: {end - start}")
#schedule, globalStudentCount, score, notAddedDict = classSchedule("testE/constraints_0", "testE/prefs_0")

file = open("mod_output.txt", "wb")
file.write(bytes("Course\tRoom\tTeacher\tTime\tStudents\n", "UTF-8"))
# schedule, globalStudentCount, score, notAddedDict = classSchedule("scripts/esemtinyc.txt", "scripts/esemtinyp.txt")
for time in schedule:
    for clss in time:
        if not clss is None:
            file.write(bytes(f"{clss}\n", "UTF-8"))

print(score)
print(notAddedDict)