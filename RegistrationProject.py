import re
from re import S

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        n = Node(data)

        if self.head == None:
            self.head = n
        else:
            n.next = head

    def popFront(self):
        n = self.head
        self.head = n.next
        return n

    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None


class Class:
    def __init__(self, class_name):
        self.name = class_name
        self.enrolled = []
        self.professor = -1
        self.time = -1

def classQ(studentPrefsFile, numClasses):
    mostPreferredClasses = []

    for i in range(numClasses):
        mostPreferredClasses.append(0)

    string = studentPrefsFile.read()
    lines = string.split('\n')
    lines = lines[1:]

    students = []

    for line in lines:
        line = re.sub('[ \t]+', ' ', line)
        pref = line.split(' ')[:1]
        students.append(pref)

    for student in students:
        for pref in student:
            mostPreferredClasses += 1

    #merge sort mostPreferredClasses and add to linked list (will make O(1) removal/re-adding sections when conflicts)

    return mostPreferredClasses, students


