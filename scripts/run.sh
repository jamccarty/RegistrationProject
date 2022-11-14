for i in 0 1 2 3 4 5 6 7 8 9
do
    c_file="testA/constraints_$i"
    p_file="testA/prefs_$i"
    if [[ "$#" == "1" ]]; then
        c_file="$1/constraints_$i"
        p_file="$1/prefs_$i"
    fi
    echo "File" $i
    python RegistrationProject.py $c_file $p_file #will need to modify RegistrationProject.py to take runtime args
    perl is_valid2.pl $c_file $p_file output.txt
done