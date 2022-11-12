#!/usr/bin/perl -w
use strict;

if (!$ARGV[0] || !$ARGV[1] || !$ARGV[2]) {

	print "$0 takes a schedule and checks that it's valid based on the constraints of the problem.\n"; 
	print "Usage:\n";
	print "$0: <constraints file> <prefs file> <schedule file>\n";
	exit 1;
}

my $cfile = $ARGV[0];
my $pfile = $ARGV[1];
my $sfile = $ARGV[2];

# to be filled by readConstraints subroutine
my $numslots;
my $numrooms;
my $numclasses;
my $numteachers;
my %roomSize = ();
my %origCourseTeacher = ();
readConstraints($cfile);

# to be filled by readPrefs subroutine
my $numstudents;
my @allStudents;
my %origStudentPrefs = ();
readPrefs($pfile);

open (SCHED, $sfile) || die "Can't open file: $sfile\n";

my %courseRoom = ();
my %courseTime = ();
my %courseStudents = ();

my %teacherCourse1 = ();
my %teacherCourse2 = ();
my %studentCourses = ();

my %timeRoom = ();

my $lineno = 0;
my $stuprefs = 0;
while (<SCHED>) {

	chomp $_;

	if ($lineno == 0) {
		if (!/^Course\tRoom\tTeacher\tTime\tStudents$/) {
			print "Header line has incorrect format.\n";
			print "Line:$_\n";
			exit 1;
		} 
	} else {
		if (!/^(\d+)\t(.+)\t(\d+)\t(\d+)\t(.*)$/) {
			print "Content line has incorrect format.\n";
			print "Line:$_\n";
			exit 1;
		} else {
			my $course = $1;
			my $room = $2;
			my $teacher = $3;
			my $time = $4;
			my $stus = $5;
			if ($stus !~ /^(\d+ )*(\d+)?$/) {
				print "Students have incorrect format.\n";
				print "Students:$1\n";
				exit 1;
			} else {
				my @students = split(/ /, $stus);
				my $classsize = $#students + 1;

				if (defined $courseRoom{$course}) {
					print "Course $course defined more than once.\n";
					print "Line:$_\n";
					exit 1;
				}

				$courseRoom{$course} = $room;

				if ($classsize > $roomSize{$room}) {
					print "Room $room is too small to hold course $course with $classsize students.\n";
					print "Line:$_\n";
					exit 1;
				}

				if ($origCourseTeacher{$course} != $teacher) {
					print "Course $course does not have the correct teacher.\n";
					print "Line:$_\n";
					exit 1;
				}

				if (! defined $teacherCourse1{$teacher}) {
					$teacherCourse1{$teacher} = $course;
				} else {
					if ($time eq $courseTime{$teacherCourse1{$teacher}}) {
						print "Teacher $teacher scheduled for two courses at time $time.\n";
						print "Line:$_\n";
						exit 1;
					}
				}

				$courseTime{$course} = $time;

				if (defined $timeRoom{$time}{$room}) {
					print "Multiple courses scheduled for time $time and room $room\n";
					print "Line:$_\n";
					exit 1;
				} else {
					$timeRoom{$time}{$room} = $course;
				}

				$courseStudents{$course} = \@students;

				foreach my $stu (@students) {
					if (defined $studentCourses{$stu}) {
						foreach my $cour (@{$studentCourses{$stu}}) {
							if ($courseTime{$cour} == $time) {
								print "Student $stu assigned to time conflicting courses $cour and $course.\n";
								print "Line:$_\n";
								exit 1;
							}
						}

						push @{$studentCourses{$stu}}, $course;

					} else {
						my @temp = ($course);
						$studentCourses{$stu} = \@temp; 
					}

					if (!inArray($course, \@{$origStudentPrefs{$stu}})) {
						print "Student $stu assigned to unrequested course $course.\n";
						print "Line:$_\n";
						exit 1;
					
					
					} 
				$stuprefs++;
				}
			}
		}
	
	}

	$lineno++;
}


print "Schedule is valid.\n";
print "Student preferences value: ", $stuprefs;

exit 0;


sub readConstraints {

	my $file = $_[0];
	open (CONSTRAINTS, $file) || die "Can't open file: $file\n";

	my $isroom = 0;
	my $isclass = 0;
	while (<CONSTRAINTS>) {
		chomp $_;
		if (/^Class Times\t(\d+)$/) {
			$numslots = $1;
		}
		if (/^Rooms\t(\d+)$/) {
			$numrooms = $1;
			$isroom = 1;
			next;
		}
		if (/^Classes\t(\d+)$/) {
			$numclasses = $1;
			$isroom = 0;
		}
		if (/^Teachers\t(\d+)$/) {
			$numteachers = $1;
			$isclass = 1;
			next;
		}
		if ($isroom) {
			my ($roomnum, $size) = split(/\t/);
			$roomSize{$roomnum} = $size;
		}
		if ($isclass) {
			my ($classnum, $classteach) = split(/\t/);
			$origCourseTeacher{$classnum} = $classteach;
		}
	}

	return;
}

sub readPrefs {
	my $file = $_[0];
	open (PREFS, $file) || die "Can't open file: $file\n";

	while (<PREFS>) {
		chomp $_;

		if (/^Students\t(\d+)$/) {
			$numstudents = $1;
			next;
		}

		if (/^(\d+)\t(.*)$/) {
			my $stu = $1;
			my @prefs = split(/ /, $2);
			$origStudentPrefs{$stu} = \@prefs;
		}
	}

	return;
}

sub inArray {
	my $item = $_[0];
	my $arr = $_[1];

	foreach my $it (@{$arr}) {
		if ($it eq $item) {
			return 1;
		}
	}

	return 0;
}
