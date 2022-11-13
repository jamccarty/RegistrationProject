import pandas as pd
import datetime
import re
import DataStructures as ds
import classroomMechanics as mech
import sys

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
        numClasses -- number of classes (integer)
        times -- array of TimeSlot() objects ;
            Each TimeSlot() object in times holds the following pieces of information:
                id = the id of the time
                start_time  - the start time, float
                end_time - the end time, float
                days_of_week - the days of the week it occurs on, array of strings
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
    count = 1 # this is the "ID"

    # initialize rooms array -- array of tuples (room size, room id)
    # (this is so that after merge sorting, each size remains paired with correct room id)
    for line in lines[2+numTimeSlots:2 + numTimeSlots + numRooms]:
        x = line.split('\t')
        # TODO: handle domains and accessibility
        new_room = mech.Room(x[0], int(x[1]), "domain", True) # ID capacity domain accesible
        rooms.append(new_room)
        count += 1
    mergeSort(rooms, 0)

    # Get Number of Classes
    loc = 2 + numTimeSlots + numRooms + 1
    x = lines[loc].split('\t')
    numClasses = int(x[1])

    # Get Number of Class Teachers
    x = lines[loc].split('\t')
    classTeachers = [] # array of classes indexed by classID (first is 0)
    classTeachers.append(0) #there is no 0 class

    # adding correct professor for each class
    for i in range(numClasses):
        loc += 1
        tc = lines[loc].split('\t')
        classTeachers.append(int(tc[1]))

    file.close() #close file
    return numTimeSlots, rooms, numClasses, times

'''
    PARAMS:
        studentsFilename -- FILE OBJECT of studentprefs.txt
        numClasses -- number of classes
    RETURNS:
        mostPreferred -- LinkedList of classes organized in descending order by how preferred they are
        students -- array of arrays. Outer array is indexed by student id, inner arrays are student preference lists
        whoPrefers -- array of arrays of students who prefer a class, indexed by class
'''
def classQ(studentsFilename, numClasses):
    # array of tuples for merge sort reasons --> will turn into LinkedList() later
    # will be organized (preference level of class, class id)
    mostPreferredClasses = []

    #array of LinkedLists of all students who prefer class, indexed by class
    whoPrefers = []
    whoPrefers.append([]) #append blank -- no class 0

    for i in range(numClasses):
        mostPreferredClasses.append(None)
        whoPrefers.append([])

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
            if mostPreferredClasses[pref-1] is None:
                mostPreferredClasses[pref-1] = Class(pref)
                mostPreferredClasses[pref-1].preferredStudents += 1
            mostPreferredClasses[pref-1].preferredStudents += 1
            whoPrefers[pref].append(i)

    # mergeSort the classes based on preference level
    mergeSort(mostPreferredClasses, 0)

    # turn mostPreferredClasses array from an array of tuples to a linked list of Class() objects
    #(will make O(1) removal/re-adding sections when conflicts)
    mostPreferred = ds.arrayToLinkedList(mostPreferredClasses)

    file.close()
    return mostPreferred, students, whoPrefers

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
def conflictSchedule(schedule, whoPrefers, studentSchedules, profSchedules, globalStudentCount):
    for r in range(len(schedule)):
        for time in range(len(schedule[r][1:])): #non esems
            currClass = schedule[r][time]
            if currClass is None:
                continue
            room = currClass.room
            maxSwappedClassStudents = []
            maxSwapTime = time
            for t2 in range(len(schedule[r][1:time])):
                curSwapStudents = []
                swapClass = schedule[r][t2]
                if swapClass is None:
                    continue
                if profSchedules[swapClass.professor].contains(time):
                    break
                for student in whoPrefers[swapClass.name]:
                    x = student
                    if not studentSchedules[x].contains(time):
                        curSwapStudents.append(x)
                if len(curSwapStudents) > room[0]:
                    break
                if len(curSwapStudents) > len(maxSwappedClassStudents):
                    maxSwappedClassStudents = curSwapStudents
                    maxSwapTime = t2
            
            if len(maxSwappedClassStudents) > len(currClass.enrolled):
                swapClass = schedule[r][maxSwapTime]
                globalStudentCount -= len(swapClass.enrolled)
                globalStudentCount -= len(currClass.enrolled)
                schedule[r][maxSwapTime] = currClass
                schedule[r][time] = swapClass
                schedule[r][maxSwapTime].schedule = maxSwappedClassStudents

                for x in maxSwappedClassStudents:
                    studentSchedules[x].remove(maxSwapTime)
                    studentSchedules[x].append(time)
                
                for x in swapClass.enrolled:
                    studentSchedules[x].remove(time)
                    if not studentSchedules[x].contains(maxSwapTime):
                        studentSchedules[x].append(maxSwapTime)

                globalStudentCount += len(schedule[r][maxSwapTime].enrolled) + len(maxSwappedClassStudents)

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
        classTeachers -- array of classes indexed by professor who teaches them
        times -- list of timeslots
    '''
    numTimeSlots, maxRoomSize, classTeachers, times = parseConstraints(constraints_filename)
    mergeSort(maxRoomSize, 0)
    
    # initialize preferred students and Class ranked lists
    classRanks, studentPrefLists, whoPrefers = classQ(students_filename, len(classTeachers)-1)
    globalStudentCount = 0

    # innit student's schedules
    studentSchedules = generateSchedules(len(studentPrefLists))
    profSchedules = generateSchedules(int(len(classTeachers) / 2))

    holdClass = ds.LinkedList()
    schedule = []

    for room in maxRoomSize:
        schedule.append([])

    for room in maxRoomSize:
        for time in range(numTimeSlots): #TODO: how do this timeSlot stuff -- which assignment is most optimal?
            if classRanks.isEmpty():
                # df = pd.DataFrame(schedule)
                # df.columns = [f'time {t}' for t in range(numTimeSlots)]
                # df.index = [f'room {r[1]}' for r in maxRoomSize]
                # print(studentPreferenceCount)
                return schedule, globalStudentCount, globalStudentCount / ((len(studentPrefLists) - 1) * 4), (len(studentPrefLists) - 1)*4

            clss = classRanks.popFront()

            skipTime = False
            while profSchedules[classTeachers[clss.name]].contains(time):
                #while profSchedules[classFacts[clss.name].professor].contains(time):
                holdClass.append(clss)
                #print(classRanks)

                if classRanks.isEmpty():
                    skipTime = True
                    break

                clss = classRanks.popFront()
            

            if skipTime == True:
                classRanks = holdClass
                continue

            if not holdClass.isEmpty():
                classRanks.merge(holdClass)

            clss.professor = classTeachers[clss.name]
            
            profSchedules[clss.professor].append(time)
            for x in whoPrefers[clss.name]:
                if len(clss.enrolled) == room[0]:
                    break
                if(not studentSchedules[x].contains(time)):
                    clss.enrolled.append(x)
                    studentSchedules[x].append(time) # TODO
                    globalStudentCount+=1

            clss.room = room
            clss.time = time
            schedule[clss.room[1] - 1].append(clss)
            # print(f"Room: {room[1]} - Class {clss.name}, prof {clss.professor}, time {time}")

    conflictSchedule(schedule, whoPrefers, studentSchedules, profSchedules, globalStudentCount)
    # df = pd.DataFrame(schedule)
    # df.columns = [f'time{t}' for t in range(numTimeSlots)]
    # df.index = [f'room {r[1]}' for r in maxRoomSize]
    return schedule, globalStudentCount, globalStudentCount / ((len(studentPrefLists) - 1) * 4), (len(studentPrefLists) - 1)*4

def main():
    file = open("output.txt", "wb")
    file.write(bytes("Course\tRoom\tTeacher\tTime\tStudents\n", "UTF-8"))
    # user_consts_file = "scripts/esemtinyc.txt"
    # user_prefs_file = "scripts/esemtinyp.txt"
    user_consts_file = ""
    user_prefs_file =  ""
    if len(sys.argv) >= 2:
        user_consts_file = sys.argv[1]
        user_prefs_file = sys.argv[2]
    else:
        sys.exit("Usage: RP_bmc.py <constriants.txt> <student_prefs.txt>")
        
    start = datetime.datetime.now().microsecond / 1000.0
    schedule, globalStudentCount, score, totalStudents = classSchedule(user_consts_file, user_prefs_file)
    end = datetime.datetime.now().microsecond / 1000.0
    print(f"Percent Assigned: {score}")
    print(f"# of Assigned Students: {globalStudentCount}\t Total Possible Assignments: {totalStudents}")
    print(f"Time (milli): {(end-start)}")

    for time in schedule:
        for clss in time:
            file.write(bytes(f"{clss}\n", "UTF-8"))

    file.close()
# main()