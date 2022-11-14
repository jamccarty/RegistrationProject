import re
import DataStructures as ds
import classroomMechanics as mech

stem_majors = ["MATH","PSYC","BIOL","PHYS","CMSC","GEOL","ECON"]
accesible_buildings = ["CAN", "CARP","DAL","GO","PK",]

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
    classDict = []

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

        if x[0][:2] in accesible_buildings or x[0][:3] in accesible_buildings:
            accesibility = True
        else:
            accesibility = False
        new_room = mech.Room(x[0], int(x[1]), domain, accesibility)
        # print(new_room.accessible)
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
    # print(classes)

    majors = []
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
        if majorContributedTo not in majors:
            majors.append(majorContributedTo)
        if tc[2] in stem_majors:
            reqdomain = mech.domain("STEM",0)
        else:
            reqdomain = mech.domain("HUM",1)
        # print(tc)
        new_class = mech.Class(int(tc[0]), requiredProfessor, majorContributedTo, reqdomain, False,i+1)
        if not(int(tc[0]) in classDict):
            classDict.append(int(tc[0]))
        # print(new_class.domain)
        classes[reqdomain.id][i+1] = new_class
    # print(loc)
    # print(len(classes))
    file.close() #close file
    # print(numClasses)
    return numTimeSlots, rooms, classes, classDict, times, majors

constraints_filename = "f2_constraints.txt"
numTimeSlots, maxRoomSize, classes, classArr, timeSlots, majors = parseConstraints(constraints_filename)

classDict = {5119: 0, 2469: 1, 1444: 2, 5724: 3, 1248: 4, 3001: 5, 3003: 6, 5727: 7, 1749: 8, 3275: 9, 7375: 10, 8500: 11, 3556: 12, 2951: 13, 4065: 14, 6023: 15, 1162: 16, 7076: 17, 7127: 18, 2935: 19, 3433: 20, 5248: 21, 7053: 22, 8496: 23, 8779: 24, 1893: 25, 7006: 26, 1767: 27, 7124: 28, 7364: 29, 8765: 30, 5206: 31, 5286: 32, 2562: 33, 7068: 34, 5227: 35, 7043: 36, 1852: 37, 1836: 38, 2160: 39, 6846: 40, 4051: 41, 1573: 42, 4888: 43, 4011: 44, 7125: 45, 7372: 46, 7374: 47, 7381: 48, 2637: 49, 3026: 50, 6502: 51, 2464: 52, 2472: 53, 8821: 54, 7398: 55, 1766: 56, 2571: 57, 4885: 58, 5258: 59, 2173: 60, 2182: 61, 3034: 62, 3465: 63, 3562: 64, 2992: 65, 3277: 66, 3525: 67, 1752: 68, 4815: 69, 1547: 70, 1560: 71, 1561: 72, 1562: 73, 7915: 74, 2394: 75, 6059: 76, 4014: 77, 6042: 78, 6044: 79, 8485: 80, 8488: 81, 3441: 82, 4017: 83, 4304: 84, 4274: 85, 7007: 86, 6026: 87, 1864: 88, 8767: 89, 8479: 90, 6036: 91, 6054: 92, 1178: 93, 1185: 94, 1838: 95, 7008: 96, 1193: 97, 6029: 98, 6860: 99, 5734: 100, 7377: 101, 7395: 102, 8763: 103, 4374: 104, 4853: 105, 7034: 106, 3442: 107, 3518: 108, 6848: 109, 5740: 110, 5741: 111, 1237: 112, 4280: 113, 3505: 114, 1151: 115, 1890: 116, 1897: 117, 3454: 118, 
1213: 119, 1845: 120, 1763: 121, 4835: 122, 1551: 123, 6865: 124, 8492: 125, 7393: 126, 1576: 127, 4808: 128, 1843: 129, 2669: 130, 4013: 131, 2151: 132, 5845: 133, 1856: 134, 3027: 135, 8441: 136, 4857: 137, 1424: 138, 2856: 139, 2872: 140, 4735: 141, 5847: 142, 1189: 143, 1862: 144, 5123: 145, 8796: 146, 2162: 147, 2164: 148, 4830: 149, 5159: 150, 4807: 151, 4359: 152, 1764: 153, 2635: 154, 8439: 155, 1442: 156, 8784: 157, 6539: 158, 6863: 159, 7902: 160, 4046: 161, 4297: 162, 8420: 163, 4282: 164, 6518: 165, 5221: 166, 2412: 167, 1194: 168, 2660: 169, 2709: 170, 8773: 171, 1847: 172, 4036: 
173, 4355: 174, 1196: 175, 2564: 176, 5282: 177, 1468: 178, 4278: 179, 1559: 180, 2668: 181, 2671: 182, 4866: 183, 3445: 184, 1566: 185, 1568: 186, 5141: 187, 7905: 188, 4879: 189, 2367: 190, 6038: 191, 6544: 192, 6585: 193, 4666: 194, 1179: 195, 4009: 196, 4739: 197, 6024: 198, 2949: 199, 2939: 200, 2945: 201, 4838: 202, 7010: 203, 6500: 204, 6508: 205, 3007: 206, 4733: 207, 5863: 208, 2420: 209, 1467: 210, 5121: 211, 7881: 212, 4027: 213, 4379: 214, 1465: 215, 7887: 216, 6555: 217, 2855: 218, 4288: 219, 4394: 220, 8470: 221, 6525: 222, 1747: 223, 1765: 224, 2149: 225, 5852: 226, 6501: 227, 5129: 228, 1755: 229, 2408: 230, 3270: 231, 4361: 232, 7877: 233, 3407: 234, 1156: 235}
classLog = []
print(f"Number of Time Slots: {numTimeSlots}")
# print(maxRoomSize.str)
# for room in maxRoomSize:
#     print(f"{room.id} \t {room.capacity}\t{room.domain}")
    # print(f"{room[1]}\t{room[0]}")
# print(classes) # ? RN it's just printing the uh. the teacher
count = 1
numClass = 0

# print(maxRoomSize)
# print(classArr)
# for domain in classes:
#     for clss in domain:
#         if clss is not None:
#             classLog.append(clss.name)
#             numClass += 1
#             if not(clss.name in classDict):
#                 print(clss.name)
#             # print(f"{count})\t{clss.name}\t{clss.professor}\t{clss.major}\t{clss.domain}")
#             # count += 1
for clss in classLog:
    if not(clss in classArr):
        print(clss)
# print(numClass)
# print(len(classDict))
# print(len(classes))
# print(timeSlots)
# for time in timeSlots:
#     print(f"{time.start_time}\t{time.end_time}\t{time.days_of_week}")
# print(majors)