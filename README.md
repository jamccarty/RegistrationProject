# RegistrationProject
A greedy algorithm designed to intake:
  - a set of student preferences for s students
  - a set of c classes and p professors (assumes each professor can teach 2 classes and that c = 2p)
  - a set of t non overlapping time slots
  - a set of r rooms and their associated sizes (i.e. how many students each room can hold)

and return a valid schedule of classes and their associated enrolled students. Runs with a complexity of O(cs + rlogr).

# Usage
Run `get_bmc_info.py` on the .csv file you wish to generate a schedule from. Then, run `RP_bmc.py` as such:

`python RP_bmc.py <constraints.txt> <student_prefs.txt>`

(Note: you cannot run this program on Haverford data)