#!/usr/bin/perl -w
use strict;
use POSIX;

my $maxroomcapacity = 1000;
my $minroomcapacity = 10;

if (!$ARGV[0] || !$ARGV[1] || !$ARGV[2] || !$ARGV[3] || !$ARGV[4] || !$ARGV[5]) {

	print "$0 takes schedule bounds and randomly creates two files for input to a schedule maker.\n";
	print "The first contains all the class-specific constrains, and the second the student class preferences.\n";
	print "Usage:\n";
	print "$0: <number of rooms> <number of classes> <number of class times> <number of students> <contraint file> <student prefs file>\n";
	exit 1;
}


my $numrooms = $ARGV[0];
my $numclasses = $ARGV[1];
my $numslots = $ARGV[2];

if ($numclasses % 2 != 0) {
	print "The number of classes must be even, since we're assuming each teacher teaches 2 classes and there cannot be fractional teachers.\n";
	exit 1;
}

my $numstudents = $ARGV[3];
my $numteachers = $numclasses / 2;
my $constraintfile = $ARGV[4];
my $prefsfile = $ARGV[5];

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
    print "The number of students must be less than the number of classes times one-forth the max room capacity (default 100, you can change the script to increase this.\n";
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
	print CONSTRAINT "$class\t$teacher\n";
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
	print PREFS "$student\t@chosenclasses\n";
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
