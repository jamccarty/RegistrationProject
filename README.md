# RegistrationProject
A greedy algorithm designed to intake:
  - a set of student preferences for s students
  - a set of c classes and p professors (assumes each professor can teach 2 classes and that c = 2p)
  - a set of t non overlapping time slots
  - a set of r rooms and their associated sizes (i.e. how many students each room can hold)

and return a valid schedule of classes and their associated enrolled students. Runs with a complexity of O(cs + rlogr).
