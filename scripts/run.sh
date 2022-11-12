for i in 0 1 2 3 4 5 6 7 8 9
do
    c_file="testF/constraints_$i"
    p_file="testF/prefs_$i"
    echo "File" $i
    python RegistrationProject.py $c_file $p_file #will need to modify RegistrationProject.py to take runtime args
done