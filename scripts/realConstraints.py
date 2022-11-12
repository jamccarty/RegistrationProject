import re
import DataStructures as ds
import classroomMechanics as mech

'''
    get_bmc_info.py constraints file format:
    Class       Times   # of Classes
        Class #     Start time - End Time (AM/PM - might want to convert to military time)   Days (MTWTHF)

    Rooms       # of Rooms
        Room Name   Capacity

    Classes     # of Classes
    Teachers    # of Teachers
        Class ID    Teacher ID      Valid Rooms [WHICH WE ARE IGNORING]   
'''

'''
parses contents of constraints.txt
PARAMS:
  file location of constraints.txt

RETURNS: numTimeSlots, rooms, classFacts, domains
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
    numTimeSlots = int(x[1]) # these are the time slots
    print(numTimeSlots)

    # TODO: get all of the time slots (as its own list of some kind - woo)

    # get number of rooms
    room = lines[1 + numTimeSlots].split('\t')
    numRooms = int(room[1]) #number of rooms total
    rooms = []

    # initialize rooms array -- array of tuples (room size, room id)
    # (this is so that after merge sorting, each size remains paired with correct room id)
    for line in lines[2+numTimeSlots:2 + numTimeSlots + numRooms]:
        x = line.split('\t')
        rooms.append((int(x[1]), x[0])) # TODO: POTENTIAL ISSUE - THERE ARE MULTIPLE OF THE SAME ROOM SIZES
    
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
    return numTimeSlots, rooms, numClasses

constraints_filename = "f2_constraints.txt"
numTimeSlots, maxRoomSize, numClasses = parseConstraints(constraints_filename)

print(f"Number of Time Slots: {numTimeSlots}")
print(maxRoomSize)
# for room in maxRoomSize:
#     print(f"{room[1]}\t{room[0]}")
print(numClasses)