# RegistrationProject
A popularity-based algorithm with conflict rescheduling designed to intake:
  - a set of student preferences for s students
  - a set of c classes and p professors (assumes each professor can teach 2 classes and that c = 2p)
  - a set of t non overlapping time slots
  - a set of r rooms and their associated sizes (i.e. how many students each room can hold)

and return a valid schedule of classes and their associated enrolled students.

# run.sh
location: ./scripts/
usage: bash run.sh (DIRECTORY)
use a directory with 10 base (no mods) files. Runs RP and is_valid 
Must be run within ./scripts/ directory

# run2.sh
location: ./scripts/
usage: bash run2.sh (DIRECTORY)
use a directory with 10 mod or base files. Runs RP2 and is_valid2
Must be run within ./scripts/ directory

# run_bmc.sh
location: ./scripts/
usage: bash run_bmc.sh (DIRECTORY)
Generates 10 schedules for each semester file of real-life Bryn Mawr data. Exports runtimes and fits to file ./scripts/testing.txt
Must be run within the ./scripts/ directory

# Generating random data
make_random_input.pl has been modified to add additional data for our constraints
For the original file, see base_make_random_input.pl
usage of our modified file: perl make_random_input.pl (num rooms) (num classes)
(num times) (num students) (NUM MAJORS) (const_file) (prefs_file)

generateRandomInstances.sh has been modified to add additional data for our constraints
For the original file, see base_generateRandomInstances.sh
usage of our modified file: bash generateRandomInstances.sh (instances) (rooms)
(classes) (times) (students) (majors)

# RegistrationProject.py
runs the base algorithm without extensions, can take in consts/prefs if desired
can only handle base (no extensions) data
usage: python RegistrationProject.py consts_file prefs_file
OR python RegistrationProject.py

# RP2.py
runs the algorithm with extensions, can take in consts/prefs if desired
can input both base and modified data
usage: python RP2.py consts_file prefs_file
OR python RP2.py
# is_valid.pl
checks if a base file (no extensions) is valid. No modifications were made
usage: perl is_valid.pl consts_file prefs_file schedule
# is_valid2.pl
checks if a mod file (extensions) is valid. Modifications were made to handle
additional data at the end of files
usage: perl is_valid2.pl consts_file prefs_file schedule
# Usage for BMC data
Run `get_bmc_info.py` on the .csv file you wish to generate a schedule from. Then, run `RP_bmc.py` as such:

`python RP_bmc.py <constraints.txt> <student_prefs.txt>`

(Note: you cannot run this program on Haverford data because our code was built
to handle the Esem constraint, which Haverford data does not work with)