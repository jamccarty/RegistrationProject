
for i in "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009" "2010" "2011" "2012" "2013" "2014"
do
    echo "
Fall" $i >> testing.txt
    for j in 1 2 3 4 5 6 7 8 9 10:
    do
        file="../brynmawr/data/Fall$i.csv"
        python get_bmc_info.py $file prefs.txt constraints.txt
        python RP_bmc.py constraints.txt prefs.txt >> testing.txt #will need to modify RegistrationProject.py to take runtime args
        # # perl is_valid2.pl constraints.txt prefs.txt mod_output.txt
    done
done
for i in "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009" "2010" "2011" "2012" "2013" "2014" "2015"
do
    echo "
Spring" $i >> testing.txt
    for j in 1 2 3 4 5 6 7 8 9 10:
    do
        file="../brynmawr/data/Spring$i.csv"
        python get_bmc_info.py $file prefs.txt constraints.txt
        python RP_bmc.py constraints.txt prefs.txt >> testing.txt #will need to modify RegistrationProject.py to take runtime args
        # # perl is_valid2.pl constraints.txt prefs.txt mod_output.txt
    done
done

