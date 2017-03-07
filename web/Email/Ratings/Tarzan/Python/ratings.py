#
# Tarzan's Diplomacy(c) Rating System
#

import os
import string
import judge_summary

Debug_Flag   = 'ON'     # if 'ON' then will show debugging information
HTML_Flag    = 'ON'     # if 'ON' then will show HTML tables

Aliases = { }     # List of Players who use OTHER (multiple) Names

Aliases[ 'michael@nat.fr'              ] = 'André'
Aliases[ 'aglennie@ns.sympatico.ca'    ] = 'Andrew Glennie'
Aliases[ 'Vinsou@club-internet.fr'     ] = 'Bonniot Vincent'
Aliases[ 'Boude@hotmail.com'           ] = 'Bouvard'
Aliases[ 'Douglas Stafford'            ] = 'Doug Stafford'
#
#  *** TYPO ***
#
Aliases[ 'Douglas Staffprd'            ] = 'Doug Stafford'
#
#  *** TYPO ***
#
Aliases[ 'Mythos'                      ] = 'Doug Stafford'
Aliases[ 'j devlin'                    ] = 'Joe Devlin'
Aliases[ 'Larry Wolff'                 ] = 'Lawrence C. Wolff'
Aliases[ 'RGA'                         ] = 'Gordon Aickin'
Aliases[ 'R. Gordon Aickin'            ] = 'Gordon Aickin'
Aliases[ 'Bamalen@aol.com'             ] = 'Len Vincent'
Aliases[ 'pierre.blais@meq.gouv.qc.ca' ] = 'Pierre Blais'
Aliases[ 'rrousse@newsbank.com'        ] = 'Robert Rousse'
Aliases[ 'karl_gign@hotmail.com'       ] = 'Spawn'

Aliases[ 'Ben "RT GM" Hines'           ] = 'Ben Hines'
Aliases[ 'Luke Ellis (GM account)'     ] = 'Luke Ellis'
Aliases[ 'Real-Time Gee-Em'            ] = 'Real-Time Gee-Em'
Aliases[ 'RT GM/Player Stephane Derdi' ] = 'Stephane Derdi'
Aliases[ 'Tarzan - Real-Time (RT) GM'  ] = 'Tarzan'
 
All_Games   = { }
All_Players = { }
Cheaters    = { }     # List of Players sharing an E-Mail Address

def Game_Sort_Index ( Powers ) :
#
# returns an Index of the Games database (All_Games) and a Sorted Index of its keys.  These
# keys are sorted from earliest date of completion to latest date of completion
#
     Index = { }
     for Game in All_Games.keys() :
          DT = All_Games[ Game ][ 'Finish' ]
          Value = string.zfill( DT[ 'Year' ], 4 )
          Value = Value + string.zfill( string.find( 'JanFebMarAprMayJunJulAugSepOctNovDec', DT[ 'Month' ] ) / 3 + 1, 2 )
          Value = Value + string.zfill( DT[ 'Day' ], 2 )
          Value = Value + DT[ 'Time' ]
          Index[ Value ] = Game
     Sort_Index = Index.keys()
     Sort_Index.sort()
     return ( Index, Sort_Index )

def Percent_Played ( From, Next_From, First_Game_Date, Game_End_Date, Winner ) :
#
# For Rating purposes any abandonment/takeover is considered to have
# occurred at the end/start of the game year.
#
# For Rating purposes a player is considered to have played in the game if:
#
#     1) he started the game (regardless of how he performed)
#     2) he shared in part (or all) of the Win
#
# Note a player who tookover a position, but went on to lose (or be eliminated)
# is considered to have NEVER played in the game (for Rating purposes).
#
     if not Winner :
          if From == First_Game_Date :
               return 1.0
          else :
               return 0.0
     else :
          if Next_From == Game_End_Date :
               return ( Next_From[ 'Year' ] - From[ 'Year' ] + 1.0 ) / ( Game_End_Date[ 'Year' ] - First_Game_Date[ 'Year' ] + 1.0 )
          else :
               return ( Next_From[ 'Year' ] - From[ 'Year' ] ) / ( Game_End_Date[ 'Year' ] - First_Game_Date[ 'Year' ] + 1.0 )

def Convert_Name ( Name ) :
#
# returns the conversion of a (single word) Name, where the first letter of the Name is
# UPPER case and the other letters of the Name are LOWER case
#
     New_Name = ''
     for Pos in range( len( Name ) ) :
          Char = Name[ Pos ]
          if Char in string.lowercase :
               if Pos == 0 :
                    Char = string.uppercase[ string.find( string.lowercase, Char ) ]
          elif Char in string.uppercase :
               if Pos != 0 :
                    Char = string.lowercase[ string.find( string.uppercase, Char ) ]
          New_Name = New_Name + Char
     return New_Name
          
def Convert_Player_Name ( Name ) :
#
# returns the converted form of a Player's Name as follows:
#
#	1) checks the Alias record to see if this Player has an alternative name
#	2) capitalizes the FIRST letter of each word in the name and put all OTHER
#	   other letters in the words in LOWER case
#
     if Aliases.has_key( Name ) :
		if Debug_Flag == 'ON' :
	          print
	          print '*****'
	          print
	          print 'Referencing %s, an Alias for %s' % ( Name, Aliases[ Name ] )
	          print
	          print '*****'
	          print
		Name = Aliases[ Name ]
     New_Name = ''
     Words = string.split( Name )
     for Word in Words :
          if New_Name != '' :
               New_Name = New_Name + ' '
          New_Name = New_Name + Convert_Name( Word )
     return New_Name
          
def Add_Player ( Player_Name, Player_EMail, Power_Played, Percent, Judge_Name, Game_Name, Game_Winners, Powers ) :
     Player_Name = Convert_Player_Name( Player_Name )
     if not ( Player_EMail in Cheaters.keys() ) :
          Cheaters[ Player_EMail ] = { }
     Cheaters[ Player_EMail ][ Player_Name ] = Judge_Name + ' ' + Game_Name
     if not ( All_Players.has_key( Player_Name ) ) :
          All_Players[ Player_Name ] = { }
          All_Players[ Player_Name ][ 'EMail' ] = [ Player_EMail ]
          All_Players[ Player_Name ][ 'Master' ] = { }
          All_Players[ Player_Name ][ 'Master' ][ 'Games' ] = { }
          for Power in Powers.keys() :
               All_Players[ Player_Name ][ Power ] = { }
               All_Players[ Player_Name ][ Power ][ 'Num Games'   ] = 0.0
               All_Players[ Player_Name ][ Power ][ 'Wins'   ] = 0.0
               All_Players[ Player_Name ][ Power ][ 'Games'  ] = { }
               All_Players[ Player_Name ][ Power ][ 'Rating' ] = 1000.0
          All_Players[ Player_Name ][ 'Total GMed' ] = 0.0
          All_Players[ Player_Name ][ 'Total Games' ] = 0.0
          All_Players[ Player_Name ][ 'Total Wins' ] = 0.0
          All_Players[ Player_Name ][ 'Overall Rating' ] = 'NR'
     elif not ( Player_EMail in All_Players[ Player_Name ][ 'EMail' ] ) :
          All_Players[ Player_Name ][ 'EMail'  ].append( Player_EMail )
     if not ( All_Players[ Player_Name ][ Power_Played ][ 'Games' ].has_key( Judge_Name + ' ' + Game_Name ) ) :
          All_Players[ Player_Name ][ Power_Played ][ 'Games' ][ Judge_Name + ' ' + Game_Name ] = { }
          All_Players[ Player_Name ][ Power_Played ][ 'Games' ][ Judge_Name + ' ' + Game_Name ][ 'Percent' ] = 0.0
     if Power_Played == 'Master' :
          All_Players[ Player_Name ][ 'Total GMed' ] = All_Players[ Player_Name ][ 'Total GMed' ] + Percent
     else :
          All_Players[ Player_Name ][ Power_Played ][ 'Num Games' ] = All_Players[ Player_Name ][ Power_Played ][ 'Num Games' ] + Percent
          All_Players[ Player_Name ][ 'Total Games' ] = All_Players[ Player_Name ][ 'Total Games' ] + Percent
     if Power_Played in Game_Winners :
          All_Players[ Player_Name ][ Power_Played ][ 'Wins' ] = All_Players[ Player_Name ][ Power_Played ][ 'Wins' ] + Percent / len( Game_Winners )
          All_Players[ Player_Name ][ 'Total Wins' ] = All_Players[ Player_Name ][ 'Total Wins' ] + Percent / len( Game_Winners )
     All_Players[ Player_Name ][ Power_Played ][ 'Games' ][ Judge_Name + ' ' + Game_Name ][ 'Percent' ] = All_Players[ Player_Name ][ Power_Played ][ 'Games' ][ Judge_Name + ' ' + Game_Name ][ 'Percent' ] + Percent
          
def Add_Game ( Judge_Name, Game_Name, Game_Press, Game_End_Date, Game_Players, Game_Winners, Game_Eliminees, Game_Start, Game_Finish, First_Game_Date, Pot, Powers ) :
     All_Games[ Judge_Name + ' ' + Game_Name ] = { }
     All_Games[ Judge_Name + ' ' + Game_Name ][ 'Press' ] = Game_Press
     All_Games[ Judge_Name + ' ' + Game_Name ][ 'End Date' ] = Game_End_Date
     All_Games[ Judge_Name + ' ' + Game_Name ][ 'Winners' ] = Game_Winners
     All_Games[ Judge_Name + ' ' + Game_Name ][ 'Eliminees' ] = Game_Eliminees
     All_Games[ Judge_Name + ' ' + Game_Name ][ 'Start' ] = Game_Start
     All_Games[ Judge_Name + ' ' + Game_Name ][ 'Finish' ] = Game_Finish
     All_Games[ Judge_Name + ' ' + Game_Name ][ 'Players' ] = { }
     All_Games[ Judge_Name + ' ' + Game_Name ][ 'Pot' ] = Pot
     for Power in [ 'Master' ] + Powers.keys() :
          All_Games[ Judge_Name + ' ' + Game_Name ][ 'Players' ][ Power ] = { }
          Index = { }
          for From_Date in Game_Players[ Power ].keys() :
               Index[ judge_summary.Game_Date_Sort_Value( judge_summary.Convert_String_to_Game_Date( From_Date ) ) ] = From_Date
          Sort_Index = Index.keys()
          Sort_Index.sort()
          for From_Date in range( len( Sort_Index ) ) :
               Player_Name = Game_Players[ Power ][ Index[ Sort_Index[ From_Date ] ] ][ 'Player' ]
               Player_EMail = Game_Players[ Power ][ Index[ Sort_Index[ From_Date ] ] ][ 'EMail' ]
               if From_Date == len( Sort_Index ) - 1 :
                    Percent = Percent_Played( judge_summary.Convert_String_to_Game_Date( Index[ Sort_Index[ From_Date ] ] ), Game_End_Date, judge_summary.Convert_String_to_Game_Date( First_Game_Date ), Game_End_Date, Power in Game_Winners )
               else :
                    Percent = Percent_Played( judge_summary.Convert_String_to_Game_Date( Index[ Sort_Index[ From_Date ] ] ), judge_summary.Convert_String_to_Game_Date( Index[ Sort_Index[ From_Date + 1 ] ] ), judge_summary.Convert_String_to_Game_Date( First_Game_Date), Game_End_Date, Power in Game_Winners )
               All_Games[ Judge_Name + ' ' + Game_Name ][ 'Players' ][ Power ][ Index[ Sort_Index[ From_Date ] ] ] = { }
               All_Games[ Judge_Name + ' ' + Game_Name ][ 'Players' ][ Power ][ Index[ Sort_Index[ From_Date ] ] ][ 'Name' ] = Player_Name
               All_Games[ Judge_Name + ' ' + Game_Name ][ 'Players' ][ Power ][ Index[ Sort_Index[ From_Date ] ] ][ 'EMail' ] = Player_EMail
               All_Games[ Judge_Name + ' ' + Game_Name ][ 'Players' ][ Power ][ Index[ Sort_Index[ From_Date ] ] ][ 'Percent' ] = Percent

def Read_Game_Summaries ( Directory, First_Game_Date, Pot, Powers ) :
     for File_Name in os.listdir( Directory ) :
          if Debug_Flag == 'ON' :
               print 'Reading in the Judge Game Summary from file < %s >' % File_Name
          ( Judge_Name, Game_Name, Game_Press, Game_Start, Game_Finish, Game_End_Date, Game_Players, Game_Winners, Game_Eliminees ) = judge_summary.Read_Game( Directory + '/' + File_Name, First_Game_Date, Powers )
          Add_Game( Judge_Name, Game_Name, Game_Press, Game_End_Date, Game_Players, Game_Winners, Game_Eliminees, Game_Start, Game_Finish, First_Game_Date, Pot, Powers )

def Process_Game ( Judge_Name, Game_Name, Game, Powers ) :
#
# A New Rating is calculated for each player in the game as follows:
#
#     New Rating = Old Rating - Amount Ante'd + Amount Won
#
# The amount won is simply a division of the "pot" (i.e. the Sum of all the
# Ante's).  If a draw occurs the "pot" is split evenly among the powers
# sharing in the draw.
#
# A Player's Ante is based on:
#
#     1) the actual Percentage the individual played (only relevant for "abandonments")
#     2) the Player's (Old) Rating relative to the other players' (Old) Ratings
#
     Sum_Ratings = 0.0
     for Power in Powers.keys() :
          for From_Date in Game[ 'Players' ][ Power ].keys() :
               Player_Name = Convert_Player_Name( Game[ 'Players' ][ Power ][ From_Date ][ 'Name' ] )
               Player_Game = All_Players[ Player_Name ][ Power ][ 'Games' ][ Judge_Name + ' ' + Game_Name ]
               Player_Game[ 'Old Rating' ] = All_Players[ Player_Name ][ Power ][ 'Rating' ]
               Sum_Ratings = Sum_Ratings + Game[ 'Players' ][ Power ][ From_Date ][ 'Percent' ] * Player_Game[ 'Old Rating' ]
     All_Games[ Judge_Name + ' ' + Game_Name ][ 'Average Rating' ] = Sum_Ratings / len( Powers.keys() )
     for Power in Powers.keys() :
          for From_Date in Game[ 'Players' ][ Power ].keys() :
               Player_Name = Convert_Player_Name( Game[ 'Players' ][ Power ][ From_Date ][ 'Name' ] )
               Player_Game = All_Players[ Player_Name ][ Power ][ 'Games' ][ Judge_Name + ' ' + Game_Name ]
               Player_Game[ 'Ante' ] = Game[ 'Pot' ] * Player_Game[ 'Percent' ] * Player_Game[ 'Old Rating' ] / Sum_Ratings
               if Power in Game[ 'Winners' ] :
                    Player_Game[ 'Winnings' ] = Player_Game[ 'Percent' ] * Game[ 'Pot' ] / len( Game[ 'Winners' ] )
               else :
                    Player_Game[ 'Winnings' ] = 0.0
               Player_Game[ 'New Rating' ] = Player_Game[ 'Old Rating' ] - Player_Game[ 'Ante' ] + Player_Game[ 'Winnings' ]
               All_Players[ Player_Name ][ Power ][ 'Rating' ] = Player_Game[ 'New Rating' ]
               All_Players[ Player_Name ][ 'Overall Rating Date' ] = Game[ 'Finish' ]

def Calculate_Players_Power_Ratings ( Powers ) :
#
# calculate each Player's Rating with EACH POWER
# 
     ( Index, Sort_Index ) = Game_Sort_Index( Powers )
     if Debug_Flag == 'ON' :
          Sorted_Powers = Powers.keys()
          Sorted_Powers.sort()
          print
          print
          Phrase = 'Average Rating with EACH Power'
          for x in range( ( len( Powers.keys() ) * 9 - 2 - len( Phrase) ) / 2 ) : 
               Phrase = ' ' + Phrase
          print '%-8s  %-s' % ( 'Game', Phrase )
          print '%8s ' % ' ',
          for Power in Sorted_Powers :
               print '   %1s    ' % Powers[ Power ][ 'Abbrev' ],
          print
          print
     for Game in Sort_Index :
          Game_Words = string.split( Index[ Game ] )
          Judge_Name = Game_Words[ 0 ]
          Game_Name = Game_Words[ 1 ]
          for Power in [ 'Master' ] + Powers.keys() :
               for From_Date in All_Games[ Judge_Name + ' ' + Game_Name ][ 'Players' ][ Power ].keys() :
                    Player = All_Games[ Judge_Name + ' ' + Game_Name ][ 'Players' ][ Power ][ From_Date ]
                    Player_Name = Convert_Player_Name( Player[ 'Name' ] )
                    Add_Player( Player_Name, Player[ 'EMail' ], Power, Player[ 'Percent' ], Judge_Name, Game_Name, All_Games[ Judge_Name + ' ' + Game_Name ][ 'Winners' ], Powers )
          if Debug_Flag == 'ON' :
               print 'Processing Game %s played on the %s Judge' % ( Game_Name, Judge_Name )
          Process_Game( Judge_Name, Game_Name, All_Games[ Judge_Name + ' ' + Game_Name ], Powers )
          if Debug_Flag == 'ON' :
               Mean_Power_Ratings = Calculate_Mean_Power_Ratings ( Powers )
               print '%-8s ' % Convert_Name( Game_Name ),
               for Power in Sorted_Powers :
                    print '%7.2f ' % eval( 'round( Mean_Power_Ratings[ Power ], 2 )' ),
               print
     if Debug_Flag == 'ON' :
          print
          print

def Calculate_Mean_Power_Ratings ( Powers ) :
#
# calculate the Mean rating for EACH POWER
#
     N = { }
     Mean_Power_Ratings = { }
     for Power in Powers.keys() : 
          N[ Power ] = 0.0
          Sum = 0.0
          for Player in All_Players.keys() :
               N[ Power ] = N[ Power ] + All_Players[ Player ][ Power ][ 'Num Games' ]
               Sum = Sum + All_Players[ Player ][ Power ][ 'Num Games' ] * All_Players[ Player ][ Power ][ 'Rating' ]
#          if round( N[ Power ],4 ) != len( All_Games.keys() ) :
#               print
#               print 'Error in Calculating the Mean Power Ratings'
#               print 'Power      = %s' % Power
#               print 'N          = %5.1f' % N[ Power ]
#               print '# of Games = %5.1f' % len( All_Games.keys() )
#               print
          Mean_Power_Ratings[ Power ] = Sum / N[ Power ]
     return Mean_Power_Ratings

def Calculate_Players_Overall_Ratings ( Mean_Power_Ratings, Powers ) :
#
# a Player's Overall Rating is a based on how his Individual Ratings
# with EACH POWER # compare to the Mean Rating for each Power
#
# an average Player's Overall Rating is 1000
#
     for Player in All_Players.keys() :
          if All_Players[ Player ][ 'Total Games' ] > 0 :
               Sum_Ratings = 0.0
               for Power in Powers.keys() :
                    Sum_Ratings = Sum_Ratings + All_Players[ Player ][ Power ][ 'Num Games' ] * All_Players[ Player ][ Power ][ 'Rating' ] / Mean_Power_Ratings[ Power ]
               All_Players[ Player ][ 'Overall Rating' ] = 1000.0 * Sum_Ratings / All_Players[ Player ][ 'Total Games' ]
     return All_Players
          
def Display_Powers_Performance ( HTML, Powers, HTML_Background_Color ) :
#
# calculates and prints a Table displaying the following information for each Power:
#
#      1) # and % of Games Won
#      2) # and % of Games Eliminated
#
     Power_Wins = { }
     Power_Eliminations = { }
     for Power in Powers.keys() :
          Power_Wins[ Power ] = 0.0
          Power_Eliminations[ Power ] = 0.0
     for Game in All_Games.keys() :
          for Power in Powers.keys() :
               if Power in All_Games[ Game ][ 'Winners' ] :
                    Power_Wins[ Power ] = Power_Wins[ Power ] + 1.0 / len( All_Games[ Game ][ 'Winners' ] )
               if All_Games[ Game ][ 'Eliminees' ].has_key( Power ) :
                    Power_Eliminations[ Power ] = Power_Eliminations[ Power ] + 1
     Num_Games = len( All_Games.keys() )
     print
     print
     if HTML :
          print '<a NAME = Stats><p><hr><p><h2>',
     print 'Powers\' Performance & Statistics',
     if HTML :
          print '</h2></p>'
     print
     print
     if HTML :
          print '<p><center><table BORDER = 10 BGCOLOR = %s>' % HTML_Background_Color
     print '    ',
     if HTML :
          print '<tr>'
          print '          <th ALIGN = LEFT>',
     print '%-10s ' % 'Power',
     if HTML :
          print '<th COLSPAN = 2>',
     print '%-11s ' % '    Wins   ',
     if HTML :
          print '%20s %s' % ( ' ', '<th COLSPAN = 2>' ),
     if HTML :
          print '%12s  <th> About these Stats' % 'Eliminations'
     else :
          print '%12s' % 'Eliminations'
     print
     for Power in Powers.keys() :
          print '    ',
          if HTML :
               print '<tr BGCOLOR = %s>' % Powers[ Power ][ 'HTML_Color' ]
               print '          <td ALIGN = LEFT>',
          print '%-10s ' % Power,
          if HTML :
               print '<td ALIGN = RIGHT>',
          print '%5.1f ' % eval( 'round( Power_Wins[ Power ], 1 )' ),
          if HTML :
               print '<td ALIGN = RIGHT>',
          print '%3d%1s ' % ( eval( 'round( 100 * Power_Wins[ Power ] / Num_Games, 0 )' ), '%' ),
          if HTML :
               print '<td ALIGN = RIGHT>',
          print '%3d ' % eval( 'round( Power_Eliminations[ Power ], 1 )' ), 
          if HTML :
               print '<td ALIGN = RIGHT>',
          print '%3d%1s' % ( eval( 'round( 100 * Power_Eliminations[ Power ] / Num_Games, 0 )' ), '%' )
     print
     if HTML :
          print
          print '     <td BGCOLOR = %s ROWSPAN = %d WIDTH = 375>' % ( HTML_Background_Color, len( Powers.keys() ) )
          print
          print '     <p>For Rating purposes a 2-way draw is worth 1/2 of a "win", a'
          print '        3-way draw is worth 1/3 of a "win", etc....</p>'
          print
          print '     <p>Thus, an N-way draw is worth 1/Nth of a "win".</p>'
          print
          print '     <p>Example:  a Power with one solo victory and a 4-way draw has 1.25 "wins"</p>'
          print
          print '     <p>Although Eliminations are <b>not</b> used in calculating a Player\'s'
          print '        Rating, these results might add some strategic insight.</p>'
          print
     print '    ',
     if HTML :
          print '<tr><th COLSPAN = %d>' % eval( 'len( Powers.keys() ) + 2' ),
     print 'Results from %d completed games' % eval( 'len( All_Games.keys() )' )
     if HTML :
          print '</table></center></p>'
     print
     print

def Display_Game_Summary ( Game_Name, Judge_Name, Powers ) :
     Game = All_Games[ Judge_Name + ' ' + Game_Name ]
     print
     print '------------------------------'
     print
     print 'Summary of Game "%s" played on the %s Judge' % ( Convert_Name( Game_Name ), Judge_Name )
     print
     Sorted_Powers = Powers.keys()
     Sorted_Powers.sort()
     Temp = ''
     for Power in Sorted_Powers :
          if Power in Game[ 'Winners' ] :
               Temp = Temp + Powers[ Power ][ 'Abbrev' ]
     if len( Temp ) == 1 :
          print '%s Solo Win' % Temp, 
     else :
         print '%s Draw' % Temp,
     print 'in %s' % judge_summary.Convert_Game_Date_to_String( Game[ 'End Date' ] )
     print
     Found = 'false'
     for Power in Sorted_Powers :
          if Game[ 'Eliminees' ].has_key( Power ) :
               print 'in %s %s was Eliminated' % ( Game[ 'Eliminees' ][ Power ], Power )
               Found = 'true'
     if Found == 'false' :
          print 'NO Powers were Eliminated'
     print
     print 'Game Started:  %2s%3s, %2s' % ( Game[ 'Start' ][ 'Month' ], Game[ 'Start' ][ 'Day' ], Game[ 'Start' ][ 'Year' ] )
     print 'Game Ended:    %2s%3s, %2s' % ( Game[ 'Finish' ][ 'Month' ], Game[ 'Finish' ][ 'Day' ], Game[ 'Finish' ][ 'Year' ] )
     print
     print
     print '%-25s   %-10s  %6s   %4s  %4s  %4s  %4s  %4s' % ( 'Player Name', 'Power', ' From ', 'Percent', 'Old Rating', 'Ante', 'Winnings', 'New Rating' )
     print
     for Power in [ 'Master' ] + Sorted_Powers :
          Index = { }
          for From_Date in Game[ 'Players' ][ Power ].keys() :
               Index[ judge_summary.Game_Date_Sort_Value( judge_summary.Convert_String_to_Game_Date( From_Date ) ) ] = From_Date
          Sort_Index = Index.keys()
          Sort_Index.sort()
          for From_Date in range( len( Sort_Index ) ) :
               Player_Name = Convert_Player_Name( Game[ 'Players' ][ Power ][ Index[ Sort_Index[ From_Date ] ] ][ 'Name' ] )
               Player_Game = All_Players[ Player_Name ][ Power ][ 'Games' ][ Judge_Name + ' ' + Game_Name ]
               print '%-25s   %-10s  %6s    %3d %1s' % ( Player_Name, Power, Index[ Sort_Index[ From_Date ] ], eval( 'round( 100 * Player_Game[ \'Percent\' ], 0 )' ), '%' ),
               if Power == 'Master' :
                    print '     %4s     %4s    %4s       %4s' % ( '  NA', '  NA', '  NA', 'NA' )
               else :
                    print '     %4d     %4d    %4d       %4d' % ( eval( 'round( Player_Game[  \'Old Rating\' ], 0 )' ), eval( 'round( Player_Game[ \'Ante\' ], 0 )' ), eval( 'round( Player_Game[ \'Winnings\' ], 0 )' ), eval( 'round( Player_Game[ \'New Rating\' ], 0 )' ) )
     print
     print 'Game \'%s\' on the %s Judge had an Average Player Rating of %4d' % ( Convert_Name( Game_Name ), Judge_Name, eval( 'round( Game[ \'Average Rating\' ], 0 )' ) )
     print
     print '------------------------------'
     print

def Display_Completed_Games ( HTML, Powers, HTML_Background_Color ) :
#
# displays a table of all the completed games
#
     print
     print
     if HTML :
          print '<a NAME = Games><p><hr><p><h2>',
     print 'Completed Games',
     if HTML :
          print '</h2></p>'
          print
     print
     if HTML :
          print '<p><center><table BORDER = 10 ALIGN = CENTER BGCOLOR = %s>' % HTML_Background_Color
     print
     if HTML :
          print '     <tr><th COLSPAN = %d>' % eval( '8 + len( Powers.keys() )' ),
     print 'Unless otherwise specified, all games are 9 SCs-for-victory, NoNMR, DIAS and Gunboat'
     if HTML :
     	print
     	print '     <tr><th COLSPAN = %2d ALIGN = LEFT> ?? Game(s) Currently Forming' % eval( '8 + len( Powers.keys() )' )
     	print '     <tr><th> Game      <th> Judge  <th> GM                         <th> Press  <th> Other<br>Paremeters   <th COLSPAN = %d> &nbsp;'  % eval( '3 + len( Powers.keys() )' )
     	print
     	print '     <tr><td> Sample    <td> USTR   <td> Tarzan                     <td> ????   <td> &nbsp;                <td COLSPAN = %d ALIGN = CENTER> <b>now forming</b>' % eval( '3 + len( Powers.keys() )' )
     	print
     	print '     <tr><th COLSPAN = 6 ALIGN = LEFT> ?? Games Currently in Progress                                                <th COLSPAN = %2d> # of SCs' % eval( 'len( Powers.keys() )' )
     	print '     <tr><th> Game      <th> Judge  <th> GM                         <th> Press  <th> Other<br>Parameters   <th> Year ',
     	for Power in Powers.keys() :
     		print '<th> %1s ' % Powers[ Power ][ 'Abbrev' ],
     	print '<th> Date<br>Started               <th Date<br>Completed'
     	print
     	print '     <tr><td> Sample    <td> USTR   <td> Tarzan                     <td> None   <td> &nbsp;'
     	print '                        <td> 1903'
     	for Power in Powers.keys() :
     		print '                        <td ALIGN = RIGHT BGCOLOR = %s> 2' % Powers[ Power ][ 'HTML_Color' ]
     	print '                        <td ALIGN = RIGHT> July  4, 1998  <td ALIGN = CENTER> <b>in progress</b>'
     	print
     	print '     <tr><th COLSPAN = %d ALIGN = LEFT>' % eval( '8 + len( Powers.keys() )' ),
     else :
          print
     print '%d Games Completed' % eval( 'len( All_Games.keys() )' )
     if HTML :
          print '     <tr><th> %-8s  <th> %-5s <th> %-25s  <th> Press  <th> Other<br>Parameters   <th> %-4s  <th COLSPAN = 2> Winner(s)                <th COLSPAN = 2> Average<br>Rating      <th> Date<br>Started          <th> Date<br>Completed' % ( 'Game', 'Judge', 'GM', 'Year' )
     else :
          print
          print '     %-8s  %-5s %-25s  Press  Other                 %-4s  Winner(s)  Average    Date       Date     ' % ( 'Game', 'Judge', 'GM', 'Year' )
          print '     %-8s  %-5s %-25s         Parameters            %-4s              Rating   Started   Completed  ' % ( ' ', ' ', ' ', ' ' )
     print
     ( Index, Sort_Index ) = Game_Sort_Index( Powers )
     Sort_Index.reverse()
     for Game in Sort_Index :
          Game_Words = string.split( Index[ Game ] )
          Judge_Name = Game_Words[ 0 ]
          Game_Name = Game_Words[ 1 ]
          GM_Name = Convert_Player_Name( All_Games[ Index[ Game ] ][ 'Players' ][ 'Master' ][ All_Games[ Index[ Game ] ][ 'Players' ][ 'Master' ].keys()[ 0 ] ][ 'Name' ] )
          Winners = ''
          for Power in Powers.keys() :
               if Power in All_Games[ Index[ Game ] ][ 'Winners' ] :
                    Winners = Winners + Powers[ Power ][ 'Abbrev' ]
          Start_Date = All_Games[ Index[ Game ] ][ 'Start' ]
          End_Date = All_Games[ Index[ Game ] ][ 'Finish' ]
          if HTML :
               print '     <tr><td>',
          print '%-8s ' % Convert_Name( Game_Name ),
          if HTML :
               print '<td>',
          print '%-4s ' % Judge_Name,
          if HTML :
               print '<td>',
          print '%-25s ' % GM_Name,
          if HTML :
               print '<td>',
          print ' %-4s ' % All_Games[ Index[ Game ] ][ 'Press' ],
          if HTML :
               print '<td>',
          print '%s ' % '&nbsp; ????',
          if HTML :
               print
               print '     %18s <td>' % ' ',
          print '%4s ' % eval( 'judge_summary.Convert_Game_Date_to_String( All_Games[ Index[ Game ] ][ \'End Date\' ] )[ 1:5 ]' ),
          if HTML :
               print '<td COLSPAN = 2 ALIGN = RIGHT>',
          print ' %7s  ' % Winners,
          if HTML :
               print '<td COLSPAN = 2 ALIGN = RIGHT>',
          print '  %4d  ' % eval( 'round( All_Games[ Index[ Game ] ][ \'Average Rating\' ], 0 )' ),
          if HTML :
               print '<td ALIGN = RIGHT>',
          print '%2s-%3s-%2s ' % ( eval( 'string.zfill( Start_Date[ \'Day\' ], 2 )' ), Start_Date[ 'Month' ], eval( 'str( Start_Date[ \'Year\' ] )[ -2: ] ' ) ),
          if HTML :
               print '<td ALIGN = RIGHT>',
          print '%2s-%3s-%2s' % ( eval( 'string.zfill( End_Date[ \'Day\' ], 2 )' ), End_Date[ 'Month' ], eval( 'str( End_Date[ \'Year\' ] )[ -2: ] ' ) )
     if HTML :
          print '</table></center></p>'
     print
     print

def Display_Player_History ( Player_Name, Mean_Power_Ratings, Powers ) :
#
# displays the Player info for all games
#
     if not All_Players.has_key( Player_Name ) :
          print
          print 'No Player History information available for %s' % Player_Name
          print
     else :
          ( Index, Sort_Index ) = Game_Sort_Index( Powers )
          print
          print '------------------------------'
          print
          print 'Player History for %s' % Player_Name
          print
          print
          Found = 'false'
          print 'Judge/Game Name GMed'
          print
          for Value in Sort_Index :
               if All_Players[ Player_Name ][ 'Master' ][ 'Games' ].has_key( Index[ Value ] ) :
                    Found = 'true'
                    Game_Words = string.split( Index[ Value ] )
                    Judge_Name = Game_Words[ 0 ]
                    Game_Name = Game_Words[ 1 ]
                    print '     %-4s %-8s' % ( Judge_Name, Convert_Name( Game_Name ) )
          if Found == 'false' :
               print '     None'
          print
          print
          print '%15s  %7s  %9s ' % ( 'Judge/Game Name', 'Percent', 'Winner(s)' ),
          for Power in Powers.keys() :
               print '%10s ' % Power,
          print '     %5s' % 'TOTAL'
          print
          print '%-15s  %7s  %9s ' % ( 'INITIALLY', ' ', ' ' ),
          for Power in Powers.keys() :
               print '      %4d ' % 1000,
          print
          print
          for Value in Sort_Index :
               Display = 'false'
               for Power_Played in Powers.keys() :
                    if All_Players[ Player_Name ][ Power_Played ][ 'Games' ].has_key( Index[ Value ] ) :
                         Game_Words = string.split( Index[ Value ] )
                         Judge_Name = Game_Words[ 0 ]
                         Game_Name = Game_Words[ 1 ]
                         print '%-4s %-8s   ' % ( Judge_Name, Convert_Name( Game_Name ) ),
                         print ' %3d %1s  ' % ( eval( 'round( 100 * All_Players[ Player_Name ][ Power_Played ][ \'Games\'][ Index[ Value ] ][ \'Percent\' ], 0)' ), '%' ),
                         Winners = ''
                         for Power in Powers.keys() :
                              if Power in All_Games[ Index[ Value ] ][ 'Winners' ] :
                                   Winners = Winners + Powers[ Power ][ 'Abbrev' ]
                         print ' %7s  ' % Winners,
                         for Power in Powers.keys() :
                              if Power == Power_Played :
                                   print '      %4d ' % eval( 'round( All_Players[ Player_Name ][ Power ][ \'Games\' ][ Index[ Value ] ][ \'New Rating\' ], 0 )' ),
                              else :
                                   print '      %4s ' % ' ',
                         print
          print
          print '%-35s ' % 'MOST RECENT Rating with EACH Power',
          for Power in Powers.keys() :
               print '      %4d ' % eval( 'round( All_Players[ Player_Name ][ Power ][ \'Rating\' ], 0 )' ),
          print
          print '%-35s ' % 'AVERAGE Rating for ALL Players',
          for Power in Powers.keys() :
               print '      %4d ' % eval( 'round( Mean_Power_Ratings[ Power ], 0 )' ),
          print
          print '%-35s  ' % '% of Rating vs. the AVERAGE Rating',
          for Power in Powers.keys() :
               print '      %3d %1s' % ( eval( 'round( 100 * All_Players[ Player_Name ][ Power ][ \'Rating\' ] / Mean_Power_Ratings[ Power ], 0 )' ), '%' ),
          print
          print
          print
          print '%-35s ' % 'Total Number of Rated Games',
          for Power in Powers.keys() :
               Num_Games = 0.0
               for Game in All_Players[ Player_Name ][ Power ][ 'Games' ].keys() :
                    Num_Games = Num_Games + All_Players[ Player_Name ][ Power ][ 'Games' ][ Game ][ 'Percent' ]
               print '     %5.1f ' % Num_Games,
          print '     %5.1f ' % All_Players[ Player_Name ][ 'Total Games' ]
          print '%-35s ' % 'Total Number of Wins',
          for Power in Powers.keys() :
               print '     %5.1f ' % All_Players[ Player_Name ][ Power ][ 'Wins' ],
          print '     %5.1f ' % All_Players[ Player_Name ][ 'Total Wins' ]
          print '%-35s ' % '% of Rated Games Won',
          for Power in Powers.keys() :
               Num_Games = 0.0
               for Game in All_Players[ Player_Name ][ Power ][ 'Games' ].keys() :
                    Num_Games = Num_Games + All_Players[ Player_Name ][ Power ][ 'Games' ][ Game ][ 'Percent' ]
               if Num_Games == 0.0 :
                    Num_Games = 1
               print '     %3d %1s ' % ( eval( 'round( 100 * All_Players[ Player_Name ][ Power ][ \'Wins\' ] / Num_Games, 0 )' ), '%' ),
          print '     %3d %1s ' % ( eval( 'round( 100 * All_Players[ Player_Name ][ \'Total Wins\' ] / All_Players[ Player_Name ][ \'Total Games\' ], 0 )' ), '%' )
          print
          print 'Overall Rating  =  %4d' % eval( 'round( All_Players[ Player_Name ][ \'Overall Rating\' ], 0 )' )
          print
          print '------------------------------'
          print

def Display_Best_Power_Players ( HTML, Powers ) :
     for Power in Powers.keys() :
	     Index = { }
	     for Player in All_Players.keys() :
			if All_Players[ Player ][ Power ][ 'Num Games' ] >= 1.0 :
				Index[ string.zfill( int( round( All_Players[ Player ][ Power ][ 'Rating' ], 0 ) ), 4 ) + ' ' + Player ] = Player
	     Sort_Index = Index.keys()
	     Sort_Index.sort()
	     Sort_Index.reverse()
	     for Count in range( len( Sort_Index ) ) :
			Rating = All_Players[ Index[ Sort_Index[ Count ] ] ][ Power ][ 'Rating' ]
			if Count == 0 :
				if HTML :
					print '<tr><td> <IMG SRC = MEDALS.GIF BORDER = 0>'
					print '                           ',
				else :
					print '%-10s' % Power
					print
					print '%3d ' % eval( 'Count + 1' ),
			else :
				if HTML :
					print '<tr><td ALIGN = RIGHT>',
				print '%3d ' % eval( 'Count + 1' ),
			if Rating == 'NR' :
				if HTML :
					print '<td ALIGN = RIGHT><font color = red>   NR</font>',
					print '<td ALIGN = RIGHT> &nbsp;    ',
				else :
					print '  NR',
			else :
				if HTML :
					print '<td ALIGN = RIGHT>                   %4d        ' % eval( 'round( Rating, 0 )' ),
					print '<td> %-20s' % Index[ Sort_Index[ Count ] ]
				else :
					print '%4d   %-20s' % ( eval( 'round( Rating, 0 )' ), Index[ Sort_Index[ Count ] ] )
	     print

def Display_Players_Stats ( Min_Total_Games, Mean_Power_Ratings, Powers, HTML_Background_Color ) :
#
# Displays the Players' Overall Ratings and Stats.  A Minimum Total # of Games
# is required to actually be considered "Rated"
#
     Index = { }
     for Player in All_Players.keys() :
          if All_Players[ Player ][ 'Overall Rating' ] == 'NR' :
               Index[ '---- ' + Player ] = Player
          elif All_Players[ Player ][ 'Total Games' ] < Min_Total_Games :
               Index[ '-' + string.zfill( int( round( All_Players[ Player ][ 'Overall Rating' ], 0 ) ), 4 ) + ' ' + Player ] = Player
          else :
               Index[ string.zfill( int( round( All_Players[ Player ][ 'Overall Rating' ], 0 ) ), 4 ) + ' ' + Player ] = Player
     Sort_Index = Index.keys()
     Sort_Index.sort()
     Sort_Index.reverse()
     print
     print '<a NAME = HoF><p><hr><p><h2>Old Salts of the Sea (the Sail Ho! Hall of Fame)</h2></p>'
     print
     print
     print '<p><center><table BORDER = 10 BGCOLOR = %s>' % HTML_Background_Color
     print '     <tr>  <th ROWSPAN = 2> Rank'
     print '           <th ROWSPAN = 2> Overall<br>Rating'
     print '           <th ROWSPAN = 2> Last<br>Rated<br>Game'
     print '           <th ROWSPAN = 2> Player'
     print '           <th COLSPAN = %d> Rating by Power' % len( Powers.keys() )
     print '           <th ROWSPAN = 2> Total<br>Wins'
     print '           <th ROWSPAN = 2> Total<br>Rated<br>Games'
     print '           <th ROWSPAN = 2> About these Stats'
     print '     <tr>'
     for Power in Powers.keys() :
          print '           <th BGCOLOR = %s> %s' % ( Powers[ Power ][ 'HTML_Color'], Power )
     print
     for Count in range( len( Sort_Index ) ) :
          Player = All_Players[ Index[ Sort_Index[ Count ] ] ]
          if Count == 0 :
               print '     <tr><td ALIGN = RIGHT> <IMG SRC = MEDALS.GIF BORDER = 0>'
               print '                                ',
          else :
               print '     <tr><td ALIGN = RIGHT> %3d ' % eval( 'Count + 1' ),
          if Player[ 'Overall Rating' ] == 'NR' :
               print '<td ALIGN = RIGHT><font color = red>   NR </font>',
               print '<td ALIGN = RIGHT> &nbsp;    ',
          else :
               if Sort_Index[ Count ][ 0 ] == '-' :
                    print '<td ALIGN = RIGHT><font color = red> %4d </font>' % eval( 'round( Player[ \'Overall Rating\' ], 0 )' ),
               else :
                    print '<td ALIGN = RIGHT>                   %4d        ' % eval( 'round( Player[ \'Overall Rating\' ], 0 )' ),
               print '<td ALIGN = RIGHT> %2s-%3s-%2s ' % ( eval( 'string.zfill( Player[ \'Overall Rating Date\' ][ \'Day\' ], 2 )' ), Player[ 'Overall Rating Date' ][ 'Month' ], eval( 'str( Player[ \'Overall Rating Date\' ][ \'Year\' ] )[ -2: ] ' ) ),
          print '<td> %-20s' % Index[ Sort_Index[ Count ] ],
          for Power in Powers.keys() :
               print '<td BGCOLOR = %s ALIGN = RIGHT>' % Powers[ Power ][ 'HTML_Color' ],
               if Player[ Power ][ 'Num Games' ] > 0.0 :
                    print '%4d ' % eval( 'round( Player[ Power ][ \'Rating\' ], 0 )' ),
               else :
                    print '%4s ' % '  NR',
          print '<td ALIGN = RIGHT> %5.1f ' % Player[ 'Total Wins' ],
          print '<td ALIGN = RIGHT> %5.1f ' % Player[ 'Total Games' ],
          print
     print
     print '     <tr><th COLSPAN = 3> &nbsp; <th ALIGN = LEFT> AVERAGE ',
     for Power in Powers.keys() :
          print '<th BGCOLOR = %s ALIGN = RIGHT> %4d' % ( Powers[ Power ][ 'HTML_Color' ], eval( 'round( Mean_Power_Ratings[ Power ], 0 )' ) ),
     print '<th> &nbsp;  <th> &nbsp;'
     print '</table></center></p>'
     print
     print

def check () :
#
# EACH variant is defined by the following parameters:
#
#     1. Powers - a dictionary of the Powers, their Abbreviations and Possessive forms
#     2. First Game Date - for example, S1901M
#     3. Pot - how many points TOTAL are in the Pot for each game
#     4. Directory Name - where the Judge Summaries are stored
#
	 
     import stnd_pow     # Load in Power info
     Powers = stnd_pow.Powers
     HTML_Background_Color = stnd_pow.HTML_Background_Color
     First_Game_Date = 'S1901M'     # Spring 1901 Movement Phase
     Pot = 350     # Amount in the "pot"
     Directory = '/home/dippouch/public_html/Email/Ratings/data'
#
#
#
     for Dir_Name in os.listdir( Directory ) :
		Read_Game_Summaries( Directory + '/' + Dir_Name, First_Game_Date, Pot, Powers )
     Calculate_Players_Power_Ratings ( Powers )
     Mean_Power_Ratings = Calculate_Mean_Power_Ratings ( Powers )
     Calculate_Players_Overall_Ratings( Mean_Power_Ratings, Powers )
     Display_Powers_Performance( HTML_Flag == 'ON', Powers, HTML_Background_Color )
     Display_Completed_Games( HTML_Flag == 'ON', Powers, HTML_Background_Color )
     if HTML_Flag == 'ON' :
          Display_Players_Stats( 4.0, Mean_Power_Ratings, Powers, HTML_Background_Color )
     Display_Best_Power_Players( HTML_Flag == 'ON', Powers )
     for Player in All_Players.keys() :
          if len( All_Players[ Player ][ 'EMail' ] ) > 1 :
               print '%s has Multiple E-Mail addresses' % Player
               print
               for Address in range( len( All_Players[ Player ][ 'EMail' ] ) ) :
                    print '     %s' % All_Players[ Player ][ 'EMail' ][ Address ]
                    print
     for EMail in Cheaters.keys() :
          if len( Cheaters[ EMail ].keys() ) > 1 :
               print 'Multiple Players are using %s as their E-Mail address' % EMail
               print
               for Player in Cheaters[ EMail ].keys() :
                    print '     %-25s     %-13s' % ( Player, Cheaters[ EMail ][ Player ] )
               print
     Display_Player_History( 'Tarzan', Mean_Power_Ratings, Powers )
     Display_Game_Summary ( 'asknot', 'FROG', Powers )
     
