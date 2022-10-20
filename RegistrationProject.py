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

def mergeSort(arr):
    if len(arr) > 1:
 
         # Finding the mid of the array
        mid = len(arr)//2
 
        # Dividing the array elements
        L = arr[:mid]
 
        # into 2 halves
        R = arr[mid:]
 
        # Sorting the first half
        mergeSort(L)
 
        # Sorting the second half
        mergeSort(R)
 
        i = j = k = 0
 
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
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
    mergeSort(arr)
    print("Sorted array is: ", end="\n")
    printList(arr)


