import pandas as pd
import time
import datetime
import re
import DataStructures as ds
import classroomMechanics as mech
import sys
import random

# STEM ID == 0, HUM (humanities) ID == 1
stem_majors = ["MATH","PSYC","BIOL","PHYS","CMSC","GEOL","ECON", "CHEM"]
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
        building = re.sub('[0-9]', '', x[0])

        if building == "PK":
            domain = mech.domain("STEM", 0)
        else:
            domain = mech.domain("HUM", 1)

        if building in accesible_buildings:
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

    class_id_dict = {} #dictionary where class_id_dict[class.name] = class.id

    # initialize list of classes
    classes.append([]) #domain 0
    classes.append([]) #domain 1
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
        isEsem = (majorContributedTo == 'EMLY')
        if isEsem == True:
            majorContributedTo = -1 #only for freshmen
        new_class = mech.Class(int(tc[0]), requiredProfessor, majorContributedTo, reqdomain, isEsem,i+1)
        class_id_dict[new_class.name] = new_class.id
        if not(int(tc[0]) in classDict):
            classDict.append(int(tc[0]))
        classes[reqdomain.id][i+1] = new_class
        count += 1
    file.close() #close file
    return numTimeSlots, rooms, classes, numClasses, classDict, majors, count, class_id_dict

'''
    Generates an array of students
    PARAMS:
        studentsFilename -- string filename of studentPreferenceList file
        majors -- list of valid majors
        classes -- list of domain arrays of classes Class() objects - classes[domain][class.id] = Class() object
    RETURNS: 
        students -- an array of student tuplets where each student[i] = (year, major, [class preferences])
'''   
def studentsArray(studentsFilename, majors, classes):
    file = open(studentsFilename)

    string = file.read()
    string = re.sub('[\n]+', '\n', string)
    lines = string.split('\n')
    lines = lines[1:] #skip first line

    students = []
    students.append([]) #for 0 student
    i = 0
    # fill students
    numAccomodations = 0
    for line in lines:
        i += 1
        if line == "":
            break
        
        line = re.sub('[\t]+', '\t', line)
        parts = line.split('\t') #parts now holds ['id', 'pref1 pref2 pref3 pref4 year major accomodations]
        line_pref = parts[1] #isolate student preferences
        year = random.randrange(1,5) # randomly assign a class year 
        major = -1
        # major = majors[random.randrange(0,len(majors))] # randomly assign a major
        # randomly assign if needs accesibility or not -- theoritically this *should* be 1% accesible students but y'know. probability! 
        accessible = random.randrange(0,100)
        if accessible == 0:
            accomodations = True
            numAccomodations += 1
        else: 
            accomodations = False 
        pref = line_pref.split(' ') #parse preferences

        if len(pref) == 0:
            break
        preferences_integers = [int(p) for p in pref if p != ""] #convert preferences to integers

        students.append((i, year, major, preferences_integers, accomodations, int(parts[0])))

    file.close()
    # print(numAccomodations)
    return students

def accessibleSchedule(schedule, rooms, numTimes, access_classes, access_esems, whoPrefers, student_schedules, prof_schedules, notAddedDict):
    access_rooms = []
    for i in range(len(access_classes)):
        access_classes[i] = ds.arrayToLinkedList(access_classes[i])
        access_esems[i] = ds.arrayToLinkedList(access_esems[i])
    num0 = 0
    num1 = 0
    accessnum0 = 0
    accessnum1 = 0
    for r in rooms:
        if r.domain.id == 0:
            num0+=1
            if r.accessible == True:
                accessnum0 += 1
        elif r.domain.id == 1:
            num1+=1
            if r.accessible == True:
                accessnum1 += 1
        if r.accessible == True:
            access_rooms.append(r)
    print(f"rooms in domain 0: {num0}, {accessnum0} accessible. rooms in domain 1 {num1}, {accessnum1} accessible")

    mergeSort(access_rooms, 1)

    taken_time_room_combos = []

    schedule = miniSchedule(schedule, access_esems, access_rooms, [0], 
                                                student_schedules, prof_schedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict, backwardsRooms = True, accessibleDomains = [accessnum0, accessnum1])
    # mech.printRoomArray(access_rooms)
    schedule= miniSchedule(schedule, access_classes, access_rooms, range(numTimes)[1:], 
                                                student_schedules, prof_schedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict, backwardsRooms = True, accessibleDomains = [accessnum0, accessnum1])

    return taken_time_room_combos

def miniSchedule(schedule, classes, maxRoomSize, timeSlots, studentSchedules, profSchedules, whoPrefers, taken_time_room_combos, notAddedDict, backwardsRooms = True, accessibleDomains = [0, 0]):
    print(f"domain 0: {classes[0].size}, domain 1: {classes[1].size}")
    holdClass = ds.LinkedList()
    room_count = 0
    time_count = 0
    for room in maxRoomSize:
        for time in timeSlots:
            if (time, room.id) in taken_time_room_combos:
                continue
            if classes[room.domain.id].isEmpty():
                continue

            clss = classes[room.domain.id].popFront()

            skipTime = False
            if clss.id == 0:
                continue
            if backwardsRooms == True:
                # i don't think len(classes) should be 2 so let me fix that and by fix that i mean throw a var in and pray it fixes shit
                # i have no fucking clue if this works
                if clss.preferredStudents > room.capacity and classes[clss.domain.id].size <= accessibleDomains[clss.domain.id] * (len(timeSlots) - time_count):
                    classes[room.domain.id].prepend(clss)
                    time_count += 1
                    continue
            infiniteLoopOption = False
            infiniteLoopCount = 0
            sizeOfClassesList = classes[room.domain.id].size
            while profSchedules[clss.professor.id].contains(time):
                # print(f"prof conflict: {time} clss {clss.name} - {clss.id} prof {clss.professor.id} {profSchedules[clss.professor.id]}")

                if classes[room.domain.id].isEmpty():
                    infiniteLoopOption = True
                holdClass.append(clss)

                if infiniteLoopOption == True:
                    classes[room.domain.id].head = None
                    classes[room.domain.id].tail = None

                notAddedDict.update({clss.name : 'professor schedule conflict'})

                if classes[room.domain.id].isEmpty():
                    skipTime = True
                    break

                if infiniteLoopCount > sizeOfClassesList:
                    holdClass.tail.next = classes[room.domain.id].head
                    holdClass.tail = classes[room.domain.id].tail
                    classes[room.domain.id].head = None
                    classes[room.domain.id].tail = None
                    skipTime = True
                    break

                clss = classes[room.domain.id].popFront()
                infiniteLoopCount += 1

            if skipTime == True:
                classes[room.domain.id] = holdClass
                time_count += 1
                continue
            if clss.name in notAddedDict:
                notAddedDict.pop(clss.name)

            if not holdClass.isEmpty():
                classes[room.domain.id].merge(holdClass)
            
            profSchedules[clss.professor.id].append(time)
            for student in whoPrefers[clss.id]:
                x = student.id
                if len(clss.enrolled) == room.capacity:
                    break
                if(not studentSchedules[x].contains(time)):
                    clss.enrolled.append(x)
                    
                    studentSchedules[x].append(time)
                    global globalStudentCount2
                    globalStudentCount2 += 1
                    
            clss.room = room
            clss.time = time
            schedule[clss.room.id - 1][time] = clss
            taken_time_room_combos.append((time, room.id))
            time_count += 1
        room_count += 1
        for r in maxRoomSize[:room_count]:
            conflictSchedule(schedule[r.id - 1], whoPrefers, studentSchedules, profSchedules)

    return schedule

# 
# modifies classes to be an array of LinkedList() objects, where each class[domain.id] = LinkedList() of classes
# to be taught in that domain
# params
#   FILE OBJECT of studentprefs.txt
#   number of classes as input
# returns
#   studentPreferences -- array of arrays. Outer array is indexed by student id, inner arrays are student preference lists
#   whoPrefers -- array of LinkedLists of students who prefer a class, indexed by class
def classQ(studentsFilename, classes, majors, numClasses, class_id_dict):
    studentPreferences = studentsArray(studentsFilename, majors, classes)

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
                tempClasses[clss.id] = clss

    # for each class in each student preference list, increment that classes preference level
    i = -1
    whoPrefers.append([]) #0 prefer class 0 which doesn't exist --> I don't know what this does and I'm too scared to change it
    for (id, year, major, preferences, accomodations, name) in studentPreferences[1:]:
        i += 1
        majors_student = []
        for pref in preferences:
            if pref not in class_id_dict:
                studentPreferences[id][3].remove(pref)
                continue
            pref_id = class_id_dict[pref]
            clss = classes[0][pref_id]
            if clss is None:
                clss = classes[1][pref_id]
            if clss is None:
                studentPreferences[id][3].remove(pref)
                continue
            majors_student.append(clss.major)
        max_major = ('', 0) #(major name, number of appearances in prefs list)
        for i in range(len(majors_student)):
            if majors_student.count(i) > max_major[1]:
                max_major = (majors_student[i], count(majors_student[i]))

        if year > 2:
            major = max_major[0]

        for pref in preferences:
            # print(class_id_dict)
            # print(pref)
            # account for if student requrests a Haverford class (which is not in our class_id_dict)
            if pref in class_id_dict:
                pref_id = class_id_dict[pref] # "trying to acess s/t it can't" or other  
                whoPrefers[pref_id].append(mech.Student(id, year, major, pref, accomodations))
                if accomodations == True and not tempClasses[pref_id] is None:
                    d = tempClasses[pref_id].domain.id
                    # tempClasses[pref].needsAccessibility = True
                    if tempClasses[pref_id].isEsem == True:
                        access_esems[d].append(tempClasses[pref_id])
                        esems[d][pref_id] = None
                        classes[d][pref_id] = None
                    else:
                        access_classes[d].append(tempClasses[pref_id])
                        classes[d][pref_id] = None
                        esems[d][pref_id] = None
                    tempClasses[pref_id] = None #no longer in tempClasses list -- in classes that need accessibility
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
                classes[clss.domain.id][clss.id].preferredStudents = len(whoPrefers[clss.id])
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
    For each room, check to see if swapping the timeslots of two classes will increase
    the number of students able to take classes they prefer. If this is true, then perform the swap

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
            if profSchedules[swapClass.professor.id].contains(time) or profSchedules[currClass.professor.id].contains(t2):
                continue
            #tally number of students who would be enrolled in swapClass if swapClass was scheduled at time
            for student in whoPrefers[swapClass.id]:
                x = student.id
                if not studentSchedules[x].contains(time):
                    if swapClass.enrolled.count(x) > 0:
                        swpStu.append(x)
                    elif not studentSchedules[x].contains(t2):
                        swpStu.append(x)

                if len(swpStu) == room.capacity:
                    break

            #tallying number of students who would be enrolled in currClass if currClass was scheduled at t2
            for student in whoPrefers[currClass.id]:
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
            profSchedules[room_schedule[time].professor.id].remove(time)
            profSchedules[room_schedule[time].professor.id].append(maxSwpIndex)

            profSchedules[room_schedule[maxSwpIndex].professor.id].remove(maxSwpIndex)
            profSchedules[room_schedule[maxSwpIndex].professor.id].append(time)

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
    numTimeSlots, maxRoomSize, classes, numClasses, classArr, majors, numProfessors, class_id_dict = parseConstraints(constraints_filename)
    # mergeSort(maxRoomSize, 0)
    # initialize preferred students and Class ranked lists

    studentPrefLists, whoPrefers, esems, access_classes, access_esems = classQ(students_filename, classes, majors, numClasses, class_id_dict)
    #old one
    # studentPrefLists, whoPrefers, esems, access_classes, access_esems = classQ(students_filename, classes, majors, classArr, class_id_dict) # if this still messes w/things, have it as numClasses instead
    # globalStudentCount = 0

    # innit student's schedules
    studentSchedules = generateSchedules(len(studentPrefLists))
    profSchedules = generateSchedules(numProfessors)

    schedule = []

    for r in range(len(maxRoomSize)):
        schedule.append([])
        for t in range(numTimeSlots):
            schedule[r].append(None) 

    notAddedDict = {} #dictionary of reasons for why each unadded class went unadded

    taken_time_room_combos = accessibleSchedule(schedule, maxRoomSize, numTimeSlots,
                                                access_classes, access_esems, whoPrefers, 
                                                studentSchedules, profSchedules, notAddedDict)
    
    #schedule esems for 0 time slot
    schedule = miniSchedule(schedule, esems, maxRoomSize, [0], 
                                                studentSchedules, profSchedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict)
    #0 non-accomodations classes for all other time slots
    schedule= miniSchedule(schedule, classes, maxRoomSize, range(numTimeSlots)[1:],
                                                studentSchedules, profSchedules, 
                                                whoPrefers, taken_time_room_combos, notAddedDict)
 
    return schedule, globalStudentCount2, globalStudentCount2 / ((len(studentPrefLists) - 1) * 4), notAddedDict, (len(studentPrefLists) - 1)*4, studentSchedules


file = open("bmc_output.txt", "wb")
file.write(bytes("Course\tRoom\tTeacher\tTime\tStudents\n", "UTF-8"))
user_consts_file = ""
user_prefs_file =  ""
if len(sys.argv) >= 2:
    user_consts_file = sys.argv[1]
    user_prefs_file = sys.argv[2]
else:
    sys.exit("Usage: RP_bmc.py <constriants.txt> <student_prefs.txt>")

 # parseConstraints(user_consts_file)
        
start = time.time() * 1000 
schedule, globalStudentCount, score, notAddedDict, totalStudents, ss = classSchedule(user_consts_file, user_prefs_file)
end = time.time() * 1000

for time in schedule:
    for clss in time:
        if not clss is None:
            enrolled_ls = " ".join(str(x) for x in clss.enrolled)
            # file.write(bytes(f"{clss}\n", "UTF-8"))
            file.write(bytes(f"{clss.name}\t{clss.room}\t{clss.professor.id}\t{clss.time}\t{enrolled_ls}\n", "UTF-8"))

print(f"Percent Assigned: {score}")
print(f"# of Assigned Students: {globalStudentCount}\t Total Possible Assignments: {totalStudents}")
print(f"Time (milli): {(end-start)}")
print(notAddedDict)

file.close()