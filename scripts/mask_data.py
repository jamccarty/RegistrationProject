import sys

###########################################################
class Data:
    def __init__(self):
        self.count = 0
        self.id_to_item = {}
        self.item_to_id = {}

    def get_item(self, id):
        if not id in self.id_to_item:
            return None
        else:
            return self.id_to_item[id]
    
    def get_id(self, item):
        if not item in self.item_to_id:
            return -1
        else:
            return self.item_to_id[item]
    
    def add_item(self, item):
        if item in self.item_to_id:
            return
        else:
            # id for item is from 1 to self.count (inclusive)
            self.item_to_id[item] = self.count + 1
            self.id_to_item[self.count + 1] = item
            self.count +=1
            return
###########################################################

def convert_time(time_str):
    time, midday = time_str.split()
    hour, minutes = time.split(":")

    if midday == "AM":
        return (int(hour), int(minutes))
    else:
        return (12 + int(hour), int(minutes))

def remove_overlapping_times(times):
    """
    takes in times in 24 hour format, process the time such 
    that we have only non-overlapping time slots
    """

def process_times():

    pass 

def process_teaching_assignment(teachings):
    """
    Takes in an array of teaching assignments, give each class
    an id, and each teacher an id from 0 to total number of 
    classes or teachers.
    """

    class_data= Data()
    teachers_data= Data()
    output = []
    for course, teacher in teachings:
        class_data.add_item(course)
        teachers_data.add_item(teacher)

        output.append([class_data.get_id(course), 
                    teachers_data.get_id(teacher)])

    return output, class_data, teachers_data

def process_contraints(input_filename):
    t = 0
    rooms = []

    mode = None
    teachings = []
    r = 0

    with open(input_filename, "r") as contraints_input:
        for line in contraints_input:
            line = line.split()
            if line[0] == "Class" and line[1] == "Times":
                t = int(line[2])
            elif line[0] == "Rooms":
                mode = "r"
            elif line[0] == "Classes":
                mode = "c"
            elif line[0] == "Teachers":
                mode = "p"

            else:
                if mode == "p":
                    teachings.append((line[0], line[1]))
                elif mode == "r":
                    rooms.append(int(line[1]))

    output, course_data, teacher_data = process_teaching_assignment(teachings)

    return t, rooms, output, course_data, teacher_data

def process_students_prefs(pref_filename, course_data):
    students_preferences = []
    preferences_cap = 0
    students_data= Data()

    with open(pref_filename, "r") as pref_input:
        for line in pref_input:
            line = line.split()

            interested = []

            for course in line[1:]:
                course_id = course_data.get_id(course)
                if course_id != -1:
                    interested.append(course_id)  
            if len(interested) > 0:
                students_preferences.append(interested)
                students_data.add_item(line[0])
                
            if len(interested) > preferences_cap:
                preferences_cap = len(interested)

    return students_preferences, students_data, preferences_cap     


def main():

    if len(sys.argv) < 5:
        print("Run this on files processed by get_bmc_info.py to convert it into a format\
        that is similar to the randomly generated data.")
        print("Example command: \n python3 mask_data.py <processed_constraints> <processed_prefs> <new_constraints> <new_prefs>")
        return

    contraints_file = sys.argv[1]
    prefs_file = sys.argv[2]

    output_constraints_file = sys.argv[3] 
    output_prefs_file = sys.argv[4]

    # print(sys.argv)

    t, rooms, teachings_assignments, course_data, teacher_data = \
        process_contraints(contraints_file)

    students_prefs, student_data, preference_cap = \
        process_students_prefs(prefs_file, 
        course_data)

    output_constraints_filename =  output_constraints_file
    output_prefs_filename = output_prefs_file
    
    output_constraints = open(output_constraints_filename, "w+")
    # print times, rooms, num classes, num teachers

    output_constraints.write("Class Times\t"+ str(t) + "\n")

    output_constraints.write("Rooms\t" + str(len(rooms)) + "\n")
    for i, capacity in enumerate(rooms):
        output_constraints.write(str(i+1) + "\t" + str(capacity) +"\n")
        
    output_constraints.write("Classes" + "\t" + str(course_data.count) + "\n")
    output_constraints.write("Teachers" + "\t" + str(teacher_data.count) + "\n")

    for course, teacher in teachings_assignments:
        output_constraints.write(str(course) + "\t" + str(teacher) + "\n")

    output_constraints.close()

    output_prefs = open(output_prefs_filename, "w+")
    output_prefs.write("Students" + "\t" + str(student_data.count) + "\n")
    print("Preferences Cap", preference_cap)
    for student, prefs in enumerate(students_prefs):
        output_prefs.write(str(student + 1) + "\t" + 
                            " ".join(str(course) for course in prefs) 
                            + "\n")
    output_prefs.close()

main()