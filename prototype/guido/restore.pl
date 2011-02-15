#!/usr/bin/env perl

use strict;

print "
Convenient script to chage the genshi path to the original \
when you check in and restore it for you once you check-in\n";

my $numArgs = $#ARGV + 1;

if($numArgs == 0){
    print_usage();
}

my $option = "";
foreach my $argnum (0 .. $#ARGV) {
    $option .= " $ARGV[$argnum]";
}

#print "$option\n";
#exit 0;

my $src  = "./start.py";
my $bak  = "$src.$$";
my $tmp = "$src.bak";
open GG, "<$src";
open GB, ">$bak";


chomp(my $username = `whoami`);
while(my $line = <GG>){
    chomp($line);
    $line =~ s#(sys.path.append\("/home/)$username("\).*)#$1dikim$2#g;
    $line =~ s#(g_home = )("$username")#$1"guido"#g;
    print GB "$line\n";
}

close GB;
close GG;

# Back up my original start.py
system("mv $src $tmp");

# Overwrite my start.py with the original path 
system("mv $bak $src");

# Check-in my codes
system("svn $option");

# Once check-in is done, my path is restored.
system("mv $tmp $src");

print "\nOK, your \"svn $option\" is done. Thanks.\n";

exit 0;

sub print_usage{
    print "
You have not put any proper arguments \

Usage: ./restore.py [up|ci|update|checkin|...]
At the option field, you can put any SVN sub commands.
\n";
    exit 0;
}

