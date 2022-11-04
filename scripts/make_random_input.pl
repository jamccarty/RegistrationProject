#!/usr/bin/perl -w
use strict;
use POSIX;

my $maxroomcapacity = 1000;
my $minroomcapacity = 10;

if (!$ARGV[0] || !$ARGV[1] || !$ARGV[2] || !$ARGV[3] || !$ARGV[4] || !$ARGV[5] || !$ARGV[6]) {

	print "$0 takes schedule bounds and randomly creates two files for input to a schedule maker.\n";
	print "The first contains all the class-specific constrains, and the second the student class preferences.\n";
	print "Usage:\n";
	print "$0: <number of rooms> <number of classes> <number of class times> <number of students> <NUMBER OF MAJORS> <contraint file> <student prefs file>\n";
	exit 1;
}


my $numrooms = $ARGV[0];
my $numclasses = $ARGV[1];
my $numslots = $ARGV[2];
my $nummajors = $ARGV[4];

if ($numclasses % 2 != 0) {
	print "The number of classes must be even, since we're assuming each teacher teaches 2 classes and there cannot be fractional teachers.\n";
	exit 1;
}
if ($nummajors > $numclasses){
	print "The number of majors must be less than or equal to the number of courses.\n";
	exit 1;
}

my $numstudents = $ARGV[3];
my $numteachers = $numclasses / 2;
my $constraintfile = $ARGV[5];
my $prefsfile = $ARGV[6];

if ($constraintfile) {
	$constraintfile =~ /^(.+)$/;
	$constraintfile = $1;
}

if ($prefsfile) {
	$prefsfile =~ /^(.+)$/;
	$prefsfile = $1;
}

my $classesperstudent = 4;

if ($numclasses * $maxroomcapacity < $numstudents*4) {
    print "The number of students must be less than the number of classes times one-fourth the max room capacity (default 100, you can change the script to increase this.\n";
    exit 1;
}

if ($numclasses > $numslots * $numrooms) {
	print "The number of classes must be no greater than the number of time slots times the number of rooms in order for all classes to be scheduled.\n";
	exit 1;
}

if ($numrooms * $maxroomcapacity * $numslots < 4 * $numstudents) {
	print "The total room capacities over all time slots must be large enough to hold all the students for 4 classes.\n";
	print "The current maximum room capacity is $maxroomcapacity - you can change the script to increase this.\n";
	exit 1;
}



open (CONSTRAINT, ">> $constraintfile") || die "Can't open file: $constraintfile\n";

print CONSTRAINT "Class Times\t$numslots\n";
print CONSTRAINT "Rooms\t$numrooms\n";
foreach my $room ((1..$numrooms)) {
	my $newval = rand();  # gives a random value between 0 and 1
	my $roomcap = floor($newval * ($maxroomcapacity - $minroomcapacity) + $minroomcapacity);  # room capacity between 10 and 100
	print CONSTRAINT "$room\t$roomcap\n";
}

print CONSTRAINT "Classes\t$numclasses\n";
print CONSTRAINT "Teachers\t$numteachers\n";
my %classestaught = ();
foreach my $class ((1..$numclasses)) {
	my $teacher = ceil(rand() * $numteachers);
	while (defined $classestaught{$teacher}  && $classestaught{$teacher}== 2) {
		$teacher = ceil(rand() * $numteachers);
	}
	#add a class major based on the number of majors from the input
	#add a class domain based on A, B, and C domains (evenly distributed)
	my $classmajor = int(rand($nummajors)) + 1;
	my $numindomain = int($nummajors / 3);
	my $classdomain = "N";
	if ($classmajor != -1){
		if ($classmajor <= $numindomain){
			$classdomain = "A";
		}
		elsif ($classmajor <= (2 * $numindomain)){
			$classdomain = "B";
		}
		else{
			$classdomain = "C";
		}
	}
	#add a classroom accessibility value (50% accessible classrooms)
	my $accessval = int(rand(2));
	print CONSTRAINT "$class\t$teacher\t$classmajor\t$classdomain\t$accessval\n";
	if (!defined $classestaught{$teacher}) {
		$classestaught{$teacher} = 1;
	} else {
		$classestaught{$teacher}++;
	}
}

close CONSTRAINT;


open (PREFS, ">> $prefsfile") || die "Can't open file: $prefsfile\n";

print PREFS "Students\t$numstudents\n";
foreach my $student ((1..$numstudents)) {
	my @chosenclasses = ();
	for my $i ((1..$classesperstudent)) {
		my $wantclass = ceil(rand() * $numclasses);
		while (inarray($wantclass, \@chosenclasses)) {
			$wantclass = ceil(rand() * $numclasses);
		}
		push @chosenclasses, $wantclass;
	}
	#add an class year for each student. 25% chance of each year
	# 1 is first year, 2 for 2nd, 3 for 3rd, 4 for 4th year
	my $classyear = int(rand(4)) + 1;
	#add a major for each student in their third or fourth year
	my $major = -1;
	if ($classyear >= 3){
		$major = int(rand($nummajors)) + 1;
	}
	#add an accessibility need. 0 means no access needed
	# 1% chance of 1 meaning student needs an accessible class
	my $accessvalue = int(rand(100)) + 1;
	if ($accessvalue > 1){
		$accessvalue = 0;
	}
	print PREFS "$student\t@chosenclasses\t$classyear\t$major\t$accessvalue\n";
}


sub inarray {
	my $val = $_[0];
	my $arr = $_[1];
	foreach my $i ((0..$#{$arr})) {
		if ($arr->[$i] == $val) {
			return 1;
		}
	}
	return 0;
}

exit 0;
