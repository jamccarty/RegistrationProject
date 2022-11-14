import re
import DataStructures as ds
import classroomMechanics as mech

stem_majors = ["MATH","PSYC","BIOL","PHYS","CMSC","GEOL","ECON"]

'''
    get_bmc_info.py constraints file format:
    Class       Times   # of Classes
        Class #     Start time - End Time (AM/PM - might want to convert to military time)   Days (MTWTHF)

    Rooms       # of Rooms
        Room Name   Capacity

    Classes     # of Classes
    Teachers    # of Teachers
        Class ID    Teacher ID    Major     Valid Rooms [WHICH WE ARE IGNORING]   
'''

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
    # print(numTimeSlots)

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

    count = 1 # this is the "ID"

    # initialize rooms array -- array of tuples (room size, room id)
    # (this is so that after merge sorting, each size remains paired with correct room id)
    for line in lines[2+numTimeSlots:2 + numTimeSlots + numRooms]:
        x = line.split('\t')
        # print(x)

        if x[0][:2] == "PK":
            domain = mech.domain("STEM", 0)
        else:
            domain = mech.domain("HUM", 1)
        new_room = mech.Room(x[0], int(x[1]), domain, True)
        rooms.append(new_room)
        count += 1
    
    # Get Number of Classes
    loc = 2 + numTimeSlots + numRooms 
    x = lines[loc].split('\t')
    # print(x)
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
    print(classes)

    # adding correct professor for each class
    # print(numClasses)
    # print(f"numClasses:{numClasses}")
    for i in range(numClasses):
        loc += 1
        # print(i)
        tc = lines[loc].split('\t')
        # print(tc)
        requiredProfessor = int(tc[1])
        majorContributedTo = tc[2]

        if tc[2] in stem_majors:
            reqdomain = mech.domain("STEM",0)
        else:
            reqdomain = mech.domain("HUM",1)
        # print(tc)
        new_class = mech.Class(int(tc[0]), requiredProfessor, majorContributedTo, reqdomain, False,i+1)
        # print(new_class.domain)
        # TODO: fix the indexing here because holy shit
        classes[reqdomain.id][i+1] = new_class
    # print(loc)
    # print(len(classes))
    file.close() #close file
    return numTimeSlots, rooms, classes, times

constraints_filename = "f2_constraints.txt"
numTimeSlots, maxRoomSize, classes, timeSlots = parseConstraints(constraints_filename)

print(f"Number of Time Slots: {numTimeSlots}")
# print(maxRoomSize.str)
# for room in maxRoomSize:
#     print(f"{room.id} \t {room.capacity}\t{room.domain}")
    # print(f"{room[1]}\t{room[0]}")
# print(classes) # ? RN it's just printing the uh. the teacher
for domain in classes:
    for clss in domain:
        if clss is not None:
            print(f"{clss.name}\t{clss.professor}\t{clss.major}\t{clss.domain}")
# print(len(classes))
# print(timeSlots)
# for time in timeSlots:
#     print(f"{time.start_time}\t{time.end_time}\t{time.days_of_week}")