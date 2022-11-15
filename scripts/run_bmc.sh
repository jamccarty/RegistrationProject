
for i in "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009" "2010" "2011" "2012" "2013" "2014" "2015"
do
    file="../brynmawr/data/Fall$i.csv"
    echo "File: Fall" $i
    python get_bmc_info.py $file prefs.txt constraints.txt
    python RP_bmc.py constraints.txt prefs.txt #will need to modify RegistrationProject.py to take runtime args
    perl is_valid2.pl constraints.txt prefs.txt mod_output.txt

    file="../brynmawr/data/Spring$i.csv"
    echo "File: Spring" $i
    python get_bmc_info.py $file prefs.txt constraints.txt
    python RP_bmc.py constraints.txt prefs.txt #will need to modify RegistrationProject.py to take runtime args
    perl is_valid2.pl constraints.txt prefs.txt mod_output.txt
done
