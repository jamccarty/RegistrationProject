directory=$(dirname -- $(readlink -fn -- "$0"))

for r in 4 10 20 40 200
do
    for s in 50 500
    do
        for i in 0 1 2 3 4 5 6 7 8 9
        do
            c_file="r${r}s${s}/constraints_$i"
            p_file="r${r}s${s}/prefs_$i"
            echo "File:" $r $s $i
            python RegistrationProject.py $c_file $p_file #will need to modify RegistrationProject.py to take runtime args
        done
    done
done