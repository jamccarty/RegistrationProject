import DataStructures as ds

'''
    Given two classes, A and B, calculate how much student overlap they have. 
    Params: 
        classes, list of classes each with a list of students who wish to take that class 
            (whoPrefers[class], where class is a linked list)
    Returns: 
        ret, a 2D Array, where for each ret[i,j], it gives the percentage of students in class i
        who want to take class j
'''
def depart_conflicts(classes):
    # initialize the returned matrix
    ret = [[0 for i in range(len(classes))] for j in range(len(classes))]
    print(len(classes))
    for i in range(len(classes)):
        classA = classes[i]
        for j in range(len(classes)):
            classB = classes[j]
            itt = classB.head
            # print(classA.size)
            while(itt != None):
                if classA.contains(itt.data):
                    ret[i][j] += 1
                itt = itt.next
            if classA.size != 0:
                ret[i][j] = ret[i][j] / (classA.size)
            else:
                ret[i][j] = 0

    return ret

# Testing
classes = []
c1 = ds.LinkedList()
c1.append(1)
c1.append(2)
c1.append(3)
# print(c1)

c2 = ds.LinkedList()
c2.append(2)
c2.append(3)
c2.append(4)
c2.append(1)

c3 = ds.LinkedList()
c3.append(1)
c3.append(4)
c3.append(5)

c4 = ds.LinkedList()
c4.append(4)
c4.append(5)
c4.append(2)
c4.append(1)

c5 = ds.LinkedList()

classes.append(c1)
classes.append(c2)
classes.append(c3)
classes.append(c4)
classes.append(c5)
# print(classes)

print(depart_conflicts(classes))