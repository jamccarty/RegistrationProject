import pandas as pd
import datetime
import re
import DataStructures as ds
import classroomMechanics as mech
import sys
import random

# STEM ID == 0, HUM (humanities) ID == 1
stem_majors = ["MATH","PSYC","BIOL","PHYS","CMSC","GEOL","ECON"]
accesible_buildings = ["CAN", "CARP","DAL","GO","PK",]
globalStudentCount2 = 0

class Class:

    def __init__(self, class_name):
        self.name = class_name
        self.enrolled = []
        self.professor = -1
        self.time = -1
        self.room = (-1, -1)
        self.preferredStudents = 0
    
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
        return f"{self.name}\t{self.room[1]}\t{self.professor}\t{self.time}\t{students}"

'''
    Parses contents of constraints.txt

    PARAMS:
    file location of constraints.txt

    RETURNS: numTimeSlots, rooms, numClasses
        numTimeSlots -- number of time slots (integer)
        rooms -- array of Room() objects - 
            Each Room() object in rooms holds the following pieces of information:
                capacity - the capacity of the room, integer
                id - the id of the room, string
        classes -- array of Class() objects:
            Each Class() object in classes holds the following pieces ofi nformation:
                name -
                professor - the professor elligable to teach that class
                major - the major the class counts towards
                domain - the comain that class falls under
                isEsem - if the class is an Esem
                id - a numerical ID for that class
        classDict -- list of all class IDs
        times -- array of TimeSlot() objects:
            Each TimeSlot() object in times holds the following pieces of information:
                id - the id of the time
                start_time  - the start time, float
                end_time - the end time, float
                days_of_week - the days of the week it occurs on, array of strings
        majors -- list of valid majors
    # TODO: add Esems
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
    numTimeSlots = int(x[1]) # these are the time slots

    times = []
    count = 0 # timeslot ID

    # get all of the timeslots
    for line in lines[1:numTimeSlots + 1]:
        x = line.split('\t')
        x_split = x[1].split(" ")
        time_spliced = []
        for i in x_split:
            if i != "" and not i.isspace():
                time_spliced.append(i)
        # get the days of the week and convert it to a list format
        days = time_spliced[4]
        days_ls = []
        if days == "M-F":
            days_ls.append("M")
            days_ls.append("T")
            days_ls.append("W")
            days_ls.append("TH")
            days_ls.append("F")
        else:
            for i in days:
                days_ls.append(i)

        # get the start time
        start_time = [] 
        start_time.append(time_spliced[0])
        start_time.append(time_spliced[1])
        sTime = " ".join(start_time)

        # get the end time
        end_time = [] 
        end_time.append(time_spliced[2])
        end_time.append(time_spliced[3])
        eTime = " ".join(end_time)

        # convert times into a class object
        time_slot = mech.TimeSlot(count, mech.Time(sTime), mech.Time(eTime), days_ls)
        times.append(time_slot)

    # get number of rooms
    room = lines[1 + numTimeSlots].split('\t')
    numRooms = int(room[1]) #number of rooms total
    rooms = []
    classes = []
    classDict = []

    count = 1 # this is the "ID"

    # initialize rooms array -- array of tuples (room size, room id)
    # (this is so that after merge sorting, each size remains paired with correct room id)
    for line in lines[2+numTimeSlots:2 + numTimeSlots + numRooms]:
        x = line.split('\t')

        if x[0][:2] == "PK":
            domain = mech.domain("STEM", 0)
        else:
            domain = mech.domain("HUM", 1)

        if x[0][:2] in accesible_buildings or x[0][:3] in accesible_buildings:
            accesibility = True
        else:
            accesibility = False
        new_room = mech.Room(count, int(x[1]), domain, accesibility, name=x[0])
        rooms.append(new_room)
        count += 1
    
    # Get Number of Classes
    loc = 2 + numTimeSlots + numRooms 
    x = lines[loc].split('\t')
    numClasses = int(x[1])

    # Get Number of Class Teachers
    loc += 1
    x = lines[loc].split('\t')

    # initialize list of classes
    classes.append([])
    classes.append([])
    for i in range(2):
        classes[i].append(None)
        for c in range(numClasses):
            classes[i].append(None)

    majors = []
    count = 1
    # adding correct professor for each class
    for i in range(numClasses):
        loc += 1
        tc = lines[loc].split('\t')
        requiredProfessor = mech.professor(int(tc[1]), count)
        majorContributedTo = tc[2]
        if majorContributedTo not in majors:
            majors.append(majorContributedTo)
        if tc[2] in stem_majors:
            reqdomain = mech.domain("STEM",0)
        else:
            reqdomain = mech.domain("HUM",1)
        new_class = mech.Class(int(tc[0]), requiredProfessor, majorContributedTo, reqdomain, False,i+1)
        if not(int(tc[0]) in classDict):
            classDict.append(int(tc[0]))
        classes[reqdomain.id][i+1] = new_class
    file.close() #close file
    return numTimeSlots, rooms, classes, numClasses, classDict, times, majors

'''
    Generates an array of students
    PARAMS:
        studentsFilename -- string filename of studentPreferenceList file
        majors -- list of valid majors
    RETURNS: 
        students -- an array of student tuplets where each student[i] = (year, major, [class preferences])
'''   
def studentsArray(studentsFilename, majors):
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
        year = random.randrange(1,5) # randomly assign a class year 
        major = majors[random.randrange(0,len(majors))] # randomly assign a major
        # randomly assign if needs accesibility or not -- theoritically this *should* be 1% accesible students but y'know. probability! 
        accessible = random.randrange(0,100)
        if accessible == 0:
            accomodations = True
        else: 
            accomodations = False 

        pref = line_pref.split(' ') #parse preferences

        if len(pref) == 0:
            break
        preferences_integers = [int(p) for p in pref if p != ""] #convert preferences to integers
        students.append((i, year, major, preferences_integers, accomodations))

    file.close()
    return students

def accessibleSchedule(schedule, rooms, timeSlots, access_classes, access_esems, whoPrefers, student_schedules, prof_schedules, notAddedDict):
    access_rooms = []
    for i in range(len(access_classes)):
        access_classes[i] = ds.arrayToLinkedList(access_classes[i])
        access_esems[i] = ds.arrayToLinkedList(access_esems[i])

    for r in rooms:
        if r.accessible == True:
            access_rooms.append(r)

    mergeSort(access_rooms, 1)

    taken_time_room_combos = []

    schedule = miniSchedule(schedule, access_esems, access_rooms, [0], 
                                                student_schedules, prof_schedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict)
    # TODO: "int object is not scriptable"
    schedule= miniSchedule(schedule, access_classes, access_rooms, timeSlots[1:], 
                                                student_schedules, prof_schedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict)

    return taken_time_room_combos

def miniSchedule(schedule, classes, maxRoomSize, timeSlots, studentSchedules, profSchedules, whoPrefers, taken_time_room_combos, notAddedDict):
    holdClass = ds.LinkedList()
    timeQ = ds.LinkedList()
    # make time FIFOQ list - help

    for room in maxRoomSize:
        clss = classes[room.domain.id].popFront()
        time = timeQ.popFront
        count = 0
        if clss is not None:
            for pt in profSchedules[clss.professor.id]:
                if time.conflicts_with(pt): # idk how timeconflicst work man
                    time = timeQ.popFront()
                    count += 1
                    if count > len(timeQ):
                        # a single "loop" of the "while profSchedules[clss.professor.id].contains(time)" thing
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
        
        for time in timeSlots:
            if (time, room.id) in taken_time_room_combos:
                continue
            if classes[room.domain.id].isEmpty():
                return schedule

            clss = classes[room.domain.id].popFront()

            skipTime = False
            if clss.id == 0:
                continue
            infiniteLoopOption = False
            while profSchedules[clss.professor.id].contains(time):
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
            
            if clss.id in notAddedDict:
                notAddedDict.pop(clss.id)

            if not holdClass.isEmpty():
                classes[room.domain.id].merge(holdClass)
            
            profSchedules[clss.professor.id].append(time)
            # print(clss.id)
            for student in whoPrefers[clss.id]:
                x = student.id
                # print(f"{x} - {studentSchedules[x]}")
                if len(clss.enrolled) == room.capacity:
                    break
                if(not studentSchedules[x].contains(time)):
                    clss.enrolled.append(x)
                    studentSchedules[x].append(time)
                    global globalStudentCount2
                    globalStudentCount2 += 1

            clss.room = room
            clss.time = time

            # print(f"{clss.room.name}\t Index: {clss.room.id}")
            schedule[clss.room.id - 1][time] = clss
            taken_time_room_combos.append((time, room.id))

        for r in maxRoomSize[:room.id]:
           conflictSchedule(schedule[r.id - 1], whoPrefers, studentSchedules, profSchedules)
    return schedule
    
'''
    PARAMS:
        studentsFilename -- FILE OBJECT of studentprefs.txt
        classes -- list of classes with all of the class's information
        majors -- list of majors
        classArr -- list of classes (just their IDs) 
    RETURNS:
        mostPreferred -- LinkedList of classes organized in descending order by how preferred they are
        students -- array of arrays. Outer array is indexed by student id, inner arrays are student preference lists
        whoPrefers -- array of arrays of students who prefer a class, indexed by class
        esems -- list of classes that are Esems
        access_classes -- classes that are accessible
        access_esems -- classes that are Esems and are accessible
'''
def classQ(studentsFilename, classes, majors, classArr):
    studentPreferences = studentsArray(studentsFilename, majors)

    #array of LinkedLists of all students who prefer class, indexed by class
    whoPrefers = []
    whoPrefers.append([]) #append blank -- no class 0
    tempClasses = [] #temporary array of all classes -- will be discarded with stack frame

    esems = []

    access_esems = [] #esems that need to be accessible, indexed by domain
    access_classes = [] #classes that need to be accessible, indexed by domain

    # print(numClasses)
    for d in range(len(classes)): #for number of domains
        esems.append([])
        esems[d].append(None) #0 class does not exist

        access_esems.append([]) #don't need to be indexed
        access_classes.append([]) #don't need to be indexed

    tempClasses.append(None) #0 class does not exist
    for domain in classes:
        for clss in domain:
            if clss is not None:
                whoPrefers.append([])
                tempClasses.append(None)
                esems[0].append(None)
                esems[1].append(None)
    for domain in classes:
        for clss in domain:
            if clss is not None:
                tempClasses[clss.id] = clss # ? CHANGED FROM clss.name TO clss.id AND I HAVE NO IDEA HOW THIS WILL AFFECT THINGS!!!

    # for each class in each student preference list, increment that classes preference level
    i = -1
    classDict = {}
    count = 0

    whoPrefers.append([]) #0 prefer class 0 which doesn't exist --> I don't know what this does and I'm too scared to change it

    classDictTest = {}
    itt = 0
    for (id, year, major, preferences, accomodations) in studentPreferences[1:]:
        for pref in preferences:
            if not(pref in classDictTest):
                classDictTest.update({pref:itt})
                class_id = itt
                itt += 1
            else: 
                class_id = classDictTest.get(pref)

    for (id, year, major, preferences, accomodations) in studentPreferences[1:]:
        i += 1
        for pref in preferences:
            if pref in classArr:
                if not (pref in classDict):
                    classDict.update({pref:count})
                    class_id = count
                    count += 1
                else:
                    class_id = classDict.get(pref)
                whoPrefers[class_id].append(mech.Student(id, year, major, pref, accomodations))
                if accomodations == True and not tempClasses[class_id] is None:
                    d = tempClasses[class_id].domain.id
                    # tempClasses[pref].needsAccessibility = True
                    if tempClasses[class_id].isEsem == True:
                        access_esems[d].append(tempClasses[class_id])
                        esems[d][class_id] = None 
                        classes[d][class_id] = None
                    else:
                        # print(f"{d}\t{class_id}\t{len(esems[d])}")
                        access_classes[d].append(tempClasses[class_id])
                        classes[d][class_id] = None
                        esems[d][class_id] = None
                    tempClasses[class_id] = None #no longer in tempClasses list -- in classes that need accessibility
    count = 0
    for clss in tempClasses:
        count += 1
        if not clss is None:
            if clss.isEsem == True:
                esems[clss.domain.id][clss.id] = clss
                esems[clss.domain.id][clss.id].preferredStudents = len(whoPrefers[clss.id])
                # esems[clss.domain.id][clss.name].needsAccessibility = clss.needsAccessibility
                classes[clss.domain.id][clss.id] = None

            else:
                # print(clss.domain.id)
                # print(clss.id)
                classes[clss.domain.id][clss.id].preferredStudents = len(whoPrefers[clss.id]) # TODO: index out of range here
                # classes[clss.domain.id][clss.name].needsAccessibility = clss.needsAccessibility

    #sort each whoPrefers[class] linked list in this order: majorSenior > majorJunior > nonMajorSenior > nonMajorJunior > Soph > Fresh
    for i in range(len(whoPrefers))[1:]:
        mergeSort(whoPrefers[i], 0)   

    for i in range(len(classes)):
        classes[i] = ds.removeBlanks(classes[i])
        mergeSort(classes[i], 0)
        # print(f"classes[{i}]: ",end="")
        # mech.printClassArray(classes[i])
        classes[i] = ds.arrayToLinkedList(classes[i])

        esems[i] = ds.removeBlanks(esems[i])
        mergeSort(esems[i], 0)
        # print(f"esems[{i}]: ",end="")
        # mech.printClassArray(esems[i])
        esems[i] = ds.arrayToLinkedList(esems[i])

        mergeSort(access_esems[i], 1)
        mergeSort(access_classes[i], 1)
        # print(f"access_classes[{i}]: ",end="")
        # mech.printClassArray(access_classes[i])

    return studentPreferences, whoPrefers, esems, access_classes, access_esems

'''
    Generates an array of LinkedList, where each LinkedList can hold time slots [person_index] has a class
    
    PARAMS: 
        size -- number of people in array (ex: number of professors)
    RETURNS:
        sched -- array of LinkedLists
    
'''
def generateSchedules(size):
    sched = []
    sched.append(ds.LinkedList()) #for 0 case class
    for i in range(size):
        sched.append(ds.LinkedList())
    return sched

#0 is greate`st -> least, 1 is least -> greatest
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
    For each room, check to see if swapping the timeslots of two classes will increase
    the number of students able to take classes they prefer. If this is true, then perform the swap
    # TODO: I don't actually know if this description is accurate or not help - Audrey

    PARAMS:
        schedule -- the assignment of classes/rooms/professors/students
        whoPrefers -- the list of student's preferences
        studentSchedules -- the list of classes that each student is assigned to
        profSchedules -- the professor-class assignment
        globalStudentCount -- the number of student's preferred classes that were able to be assigned
'''
def conflictSchedule(room_schedule, whoPrefers, studentSchedules, profSchedules):
    for time in range(len(room_schedule))[1:]: #non esems
        currClass = room_schedule[time]
        orgStu = []
        maxSwpStu = ([], [])
        maxSwpLen = -1
        maxSwpIndex = -1

        if currClass is None:
            continue
        room = currClass.room

        for t2 in range(len(room_schedule[:time]))[1:]: #no esems
            swapClass = room_schedule[t2] #class currClass would be swapping spots with
            swpStu = [] #students that would be enrolled in the swapClass at time t2
            if swapClass is None: #if t2 has a class scheduled
                continue #TODO we should still probably check to see if swapping currClass to this time would increase the number of enrolled students
            if profSchedules[swapClass.professor].contains(time) or profSchedules[currClass.professor].contains(t2):
                continue
            #tally number of students who would be enrolled in swapClass if swapClass was scheduled at time
            for student in whoPrefers[swapClass.name]:
                x = student.id
                if not studentSchedules[x].contains(time):
                    if swapClass.enrolled.count(x) > 0:
                        swpStu.append(x)
                    elif not studentSchedules[x].contains(t2):
                        swpStu.append(x)

                if len(swpStu) == room.capacity:
                    break

            #tallying number of students who would be enrolled in currClass if currClass was scheduled at t2
            for student in whoPrefers[currClass.name]:
                x = student.id
                if not studentSchedules[x].contains(t2):
                    if currClass.enrolled.count(x) > 0:
                        orgStu.append(x)
                    elif not studentSchedules[x].contains(time):
                        orgStu.append(x)
                
                if len(orgStu) == room.capacity:
                    break
            
            #if the number of total students enrolled would be greater if swapClass and currClass swapped times,
            swpLen = len(orgStu) + len(swpStu)
            orgLen = len(currClass.enrolled) + len(swapClass.enrolled)
            if swpLen > orgLen: #TODO we should also probably have some sort of maxOrgLen and maxOrgStu array as well, since we've already calculated them
                if swpLen > maxSwpLen:
                    maxSwpLen = swpLen
                    maxSwpStu = (orgStu, swpStu)
                    maxSwpIndex = t2
            orgStu = []
            swpStu = []
        if maxSwpIndex != -1:
            global globalStudentCount2
            globalStudentCount2 -= len(room_schedule[time].enrolled)
            globalStudentCount2 -= len(room_schedule[maxSwpIndex].enrolled)

            #set new enrollments when classes swap times
            room_schedule[time].enrolled = maxSwpStu[0]
            room_schedule[maxSwpIndex].enrolled = maxSwpStu[1]

            #edit professors' schedules to hold new times, get rid of old times
            profSchedules[room_schedule[time].professor].remove(time)
            profSchedules[room_schedule[time].professor].append(maxSwpIndex)

            profSchedules[room_schedule[maxSwpIndex].professor].remove(maxSwpIndex)
            profSchedules[room_schedule[maxSwpIndex].professor].append(time)

            #edit enrolled students' schedules to reflect new times
            for student in room_schedule[time].enrolled:
                studentSchedules[student].remove(time)
                studentSchedules[student].append(maxSwpIndex)
            for student in room_schedule[maxSwpIndex].enrolled:
                studentSchedules[student].remove(maxSwpIndex)
                studentSchedules[student].append(time)
                
            globalStudentCount2 += len(room_schedule[time].enrolled) + len(room_schedule[maxSwpIndex].enrolled)
            room_schedule[time], room_schedule[maxSwpIndex] = room_schedule[maxSwpIndex], room_schedule[time]
            room_schedule[time].time = time
            room_schedule[maxSwpIndex].time = maxSwpIndex

'''
    Given a set of constraints and student preferences, it creates a valid schedule

    PARAMS:
        constraints_filename -- the constraints file
        students_filename -- the studens preference file
    RETURNS: schedule, globalStudentCount, score, totalStudents
        schedule -- the produced class/room/teacher/student assignemnts
        globalStudentCount -- the amount of student's preferences that were assigned
        score -- percentage of how many student's preference that were able to be assigned
        totalStudents -- the total amount of student preferences
'''
def classSchedule(constraints_filename, students_filename):
    '''
        numTimeSlots - integer, number of time slots
        rooms -- unsorted linked list of rooms and associated sizes (size, room#)
        class -- array of classes indexed by professor who teaches them
        classArr -- list of classes (just their IDs)
        times -- list of timeslots
        majors -- list of valid majors
    '''
    numTimeSlots, maxRoomSize, classes, numClasses, classArr, times, majors = parseConstraints(constraints_filename)
    # mergeSort(maxRoomSize, 0)
    # initialize preferred students and Class ranked lists
    studentPrefLists, whoPrefers, esems, access_classes, access_esems = classQ(students_filename, classes, majors, classArr) # if this still messes w/things, have it as numClasses instead
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
    # TODO: these needs to be converted to the times array - how? I don't know man
    taken_time_room_combos = accessibleSchedule(schedule, maxRoomSize, numTimeSlots,
                                                access_classes, access_esems, whoPrefers, 
                                                studentSchedules, profSchedules, notAddedDict)
    #schedule esems for 0 time slot
    schedule = miniSchedule(schedule, esems, maxRoomSize, [0], 
                                                studentSchedules, profSchedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict)
    #0 non-accomodations classes for all other time slots
    schedule= miniSchedule(schedule, classes, maxRoomSize, times[1:],
                                                studentSchedules, profSchedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict)

    conflictSchedule(schedule, whoPrefers, studentSchedules, profSchedules, globalStudentCount)
 
    return schedule, globalStudentCount2, globalStudentCount2 / ((len(studentPrefLists) - 1) * 4), notAddedDict, (len(studentPrefLists) - 1)*4, studentSchedules

def main():
    file = open("output.txt", "wb")
    file.write(bytes("Course\tRoom\tTeacher\tTime\tStudents\n", "UTF-8"))
    user_consts_file = ""
    user_prefs_file =  ""
    if len(sys.argv) >= 2:
        user_consts_file = sys.argv[1]
        user_prefs_file = sys.argv[2]
    else:
        sys.exit("Usage: RP_bmc.py <constriants.txt> <student_prefs.txt>")
        
    start = float(datetime.datetime.now().microsecond / 1000.0)
    schedule, globalStudentCount, score, notAddedDict, totalStudents, ss = classSchedule(user_consts_file, user_prefs_file)
    end = float(datetime.datetime.now().microsecond / 1000.0)

    for time in schedule:
        for clss in time:
            if not clss is None:
                file.write(bytes(f"{clss}\n", "UTF-8"))

    print(f"Percent Assigned: {score}")
    print(f"# of Assigned Students: {globalStudentCount}\t Total Possible Assignments: {totalStudents}")
    print(f"Time (milli): {(end-start)}")
    print(notAddedDict)

    file.close()
main()