class LinkedList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self) -> str:
        s = ""
        loc = self.head

        while loc != None:
            s += f" -> {loc.data}"
            loc = loc.next
        
        return s

    #converts LinkedList() to array
    #WARNING, deletes contents of LinkedList()
    def toArray(self):
        array = []

        while not self.isEmpty():
            array.append(self.popFront())

        return array

    def prepend(self, data):
        n = self.Node(data)
        self.size += 1

        if self.head == None:
            self.head = n
            self.tail = n
        else:
            n.next = self.head
            self.head.prev = n
            self.head = n
    
    def append(self, data):
        n = self.Node(data)
        self.size += 1

        if self.tail == None:
            self.head = n
            self.tail = n
        else:
            self.tail.next = n
            n.prev = self.tail
            self.tail = n

    def popFront(self):
        self.size -= 1
        if self.head == None:
            return None
        if self.head.next == None:
            n = self.head
            self.head = None
            self.tail = None
            return n.data
        
        n = self.head

        if not n.next == None:
            self.head = n.next
        return n.data
    
    # merge two linked lists so that A->B
    def merge(self, A):
        if self.isEmpty():
            self.head = A.head
            self.tail = A.tail
            A.head = None
            A.tail = None
        else:
            self.head.prev = A.tail
            A.tail.next = self.head
            self.head = A.head
            A.head = None
            A.tail = None     
            self.size += A.size
            A.size = 0

    def contains(self, data):
        loc = self.head

        while loc != None:
            if loc.data == data:
                return True
            loc = loc.next
        
        return False

    def isEmpty(self):
        return self.head == None


def arrayToLinkedList(array):
    LL = LinkedList()

    for x in array:
        if not x is None:
            LL.append(x)
    
    return LL

def removeBlanks(array):
    new_array = []
    for x in array:
        if not x is None:
            new_array.append(x)
    return new_array

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
