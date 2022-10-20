import re
from re import S
import queue

class LinkedList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self):
        self.head = None

    def __str__(self) -> str:
        s = ""
        loc = self.head

        while loc != None:
            s += f" -> {loc.data}"
            loc = loc.next
        
        return s

    def append(self, data):
        n = self.Node(data)

        if self.head == None:
            self.head = n
        else:
            n.next = self.head
            self.head = n

    def popFront(self):
        n = self.head
        self.head = n.next
        return n

class Class:
    def __init__(self, class_name):
        self.name = class_name
        self.enrolled = []
        self.professor = -1
        self.time = -1
        self.preferredStudents = 0

    def __str__(self):
        return f"{self.name}"

def classQ(studentPrefsFile, numClasses):
    mostPreferredClasses = []

    for i in range(numClasses):
        mostPreferredClasses.append((0, i))

    string = studentPrefsFile.read()
    lines = string.split('\n')
    lines = lines[1:]

    students = []

    for line in lines:
        line = re.sub('[ \t]+', ' ', line)
        pref = line.split(' ')[1:]
        prefno = [int(p) for p in pref]
        students.append(prefno)

    for student in students:
        for pref in student:
            mostPreferredClasses[pref-1] = (mostPreferredClasses[pref - 1][0] + 1, pref)

    mergeSort(mostPreferredClasses, 1)
    mostPreferred = LinkedList()
    #merge sort mostPreferredClasses and add to linked list 
    #(will make O(1) removal/re-adding sections when conflicts)

    for (pref, id) in mostPreferredClasses:
        c = Class(id)
        c.preferredStudents = pref
        mostPreferred.append(c)

    return mostPreferred, students

def roomQ(rooms):
    # input: list of rooms - [size, room #] (tuple)
    sorted_rooms = mergeSort(rooms, 0)
    ret_list = LinkedList()

    for i in range(len(sorted_rooms)):
        ret_list.append(sorted_rooms[i])

    return ret_list

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
 
# Code to print the list
def printList(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()
 
 
# Driver Code
if __name__ == '__main__':
    arr = [12, 11, 13, 5, 6, 7]
    print("Given array is", end="\n")
    printList(arr)
    mergeSort(arr,1)
    print("Sorted array is: ", end="\n")
    printList(arr)

stud = open("../basic/demo_studentprefs.txt")
li, s = classQ(stud, 14)


