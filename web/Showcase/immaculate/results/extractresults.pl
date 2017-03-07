#!/usr/bin/perl
my $printing = 0;
my ($gamename, $power);
my ($phase, $year, $season);
my ($pressFlag, $temp, $longTemp, $removeBlanks, $color);
my %colors = qw|Austria ff0000 England 0000cc France 00cccc Germany 808080
  Italy	008800 Russia  ff00ff Turkey bbbb00|;
my $messageNum = 0;
my ($top, $bottom, $t, $b) = ("","");

if (-e "_top_.html") {
  open INFILE, "<_top_.html" || die "Can't read _top_.html";
  $top = join "", <INFILE>;
  close INFILE;
} else { die "Can't find _top_.html"; }
if (-e "_bottom_.html") {
  open INFILE, "<_bottom_.html" || die "Can't read _bottom_.html";
  $bottom = join "", <INFILE>;
  close INFILE;
} else { die "Can't find _bottom_.html"; }

foreach (<>) {
  
  if (($phase, $temp, $longTemp, $temp, $gamename) = /^(\w+) (orders|results) for (\w+) of (\d{4}).\s*\((\w+)\./) {
    ($temp = substr($longTemp, 0, 1)) =~ tr/W/F/;
    
    if ($year . $season ne $4 . $temp) { # new season
      ($season, $year) = ($temp, $4);
      print OUTFILE "$bottom" if defined OUTFILE;
      open OUTFILE, ">${year}\L${season}.html\E";
      ($t = $top) =~ s/!SEASON!/$longTemp/;
      $t =~ s/!YEAR!/$year/;
      print OUTFILE "$t";
      print OUTFILE "<p><center><table border=3 width=80%><tr align=center valign=middle><td><font color=FF0000 size=+2>\n".
	"Results for $longTemp of $year in $gamename\n" .
	  "</font></td></tr></table></center>\n";
    }
    print OUTFILE "<p><font color=FF0000 size=+1>$phase</font>\n";
    $printing = 1;
    next;
  }		 
  
  if ((/^The game is over/) || (/^The next phase of/)) {
    $printing = 0;
    next;
  }	
  
  if ($printing) {
    s|(Aus\w+)|<font color=$colors{'Austria'}>$1</font>|g;
    s|(Eng\w+)(?!\w* Cha)|<font color=$colors{'England'}>$1</font>|g;
    s|(Fr[ae]\w+)|<font color=$colors{'France'}>$1</font>|g;
    s|(Ger\w+)|<font color=$colors{'Germany'}>$1</font>|g;
    s|(Ita\w+)|<font color=$colors{'Italy'}>$1</font>|g;
    s|(Rus\w+)|<font color=$colors{'Russia'}>$1</font>|g;
    s|(Tur\w+)|<font color=$colors{'Turkey'}>$1</font>|g;
    s|->|<b>=></b>|g;
    s|(\(\*.+?\*\))|<i>$1</i>|g;
    $_ = "$_<BR>";
    print OUTFILE;
  }		 
}

print OUTFILE "$bottom";

