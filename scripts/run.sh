for i in 0 1 2 3 4 5 6 7 8 9
do
    c_file="ta/ta_cs_400/constraints_$i"
    p_file="ta/ta_cs_400/prefs_$i"
    echo "File" $i
    python RegistrationProject.py $c_file $p_file #will need to modify RegistrationProject.py to take runtime args
    perl is_valid2.pl $c_file $p_file output.txt
done