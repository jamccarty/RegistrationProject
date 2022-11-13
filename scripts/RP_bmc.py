import pandas as pd
import datetime
import re
import DataStructures as ds
import classroomMechanics as mech
import sys
import get_bmc_info as bmc

'''
parses contents of constraints.txt

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
    print(numTimeSlots)

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
        new_room = mech.Room(x[0], count, int(x[1]))
        rooms.append(new_room)
        count += 1
    # TODO: Merge Sort lines here?

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

''' If we input, for example, "Fall2000.csv" the command line will still say:
        Usage: RP_bmc.py <enrollment.csv> <student_prefs.txt> <constraints.txt>
    and will create a <student_prefs.txt> <constraints.txt> regardless so I think it's safe to assume
    that the csv has been run through get_bmc_info.py and we can just take the resulting prefs and constraints file
        - Audrey
'''
def parse_bmc_constraints(file_name):
    data_li = bmc.get_data_list_of_dicts(file_name)
    room_sizes = bmc.get_room_sizes(data_li)
    rooms = []
    count = 1

    for room_name in room_sizes:
        new_room = mech.Room(room_name, count, room_sizes[room_name])
        rooms.append(new_room)
        count += 1
    
    mergeSort(rooms, 0)
    print(rooms)

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
 
constraints_filename = "Fall2000.csv"
parse_bmc_constraints(constraints_filename)

# print(f"Number of Time Slots: {numTimeSlots}")
# print(maxRoomSize)
# # for room in maxRoomSize:
# #     print(f"{room[1]}\t{room[0]}")
# print(numClasses)