for i in 0 1 2 3 4 5 6 7 8 9
do
    c_file="testA/constraints_$i"
    p_file="testA/prefs_$i"
    echo $i
    python RP2.py $c_file $p_file #will need to modify RegistrationProject.py to take runtime args
done