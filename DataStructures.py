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
            array.append(self.popFront().data)

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
            return n
        
        n = self.head

        if not n.next == None:
            self.head = n.next
        return n
    
    # merge two linked lists so that A->B
    def merge(self, A):
        self.tail.next = A.head
        A.head.prev = self.tail
        A.head = None
        self.tail = A.tail
        A.tail = None
        self.size += A.size
        

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
        LL.append(x)
    
    return LL
