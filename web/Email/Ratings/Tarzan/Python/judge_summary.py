#
# Read in Game Summary sent by the Judge
#
# the following is returned:
#
# Judge Name
# Game Name
# Game Start              Year, Month, Day, Time
# Game End                Year, Month, Day, Time
# Game Date Ended         for example:  S190R, F1911B
# Players in the Game     { Power : Name : { E-Mail Address, Year/Season/Phase tookover Power }, ... }
# Winners                 [ Power Names ... ]

import string

def Convert_String_to_Game_Date ( Date ) :
#
# return the Year, Season ( Sping, Fall or Winter ) and Phase ( Moves, Retreats, Builds )
#
# the Date is in the following format:
#
#      SYYYYP,  where S = Season, YYYY = Year, P = Phase
#
#      examples:   S1901M, F1917B, F1911B
#
#      Note:  U = Summer, W = Winter
#
     Year = string.atoi( Date[ 1:5 ] )
     if Date[ 0 ] == 'S' :
          Season = 'Spring'
     elif Date[ 0 ] == 'F' :
          Season = 'Fall'
     elif Date[ 0 ] == 'W' :
          Season = 'Winter'
     else :
          print 'Invalid Game Season designated in the Game Date %s' % Date
     if Date[ 5 ] == 'M' :               
          Phase = 'Moves'
     elif Date[ 5 ] == 'R' :
          Phase = 'Retreats'
     elif Date[ 5 ] == 'B' :
          Phase = 'Builds'
     else :
          print 'Invalid Game Phase designated in the Game Date %s' % Date
     return { 'Year' : Year, 'Season' : Season, 'Phase' : Phase }

def Convert_Game_Date_to_String ( String ) :
#
# returns a Game Date in the following format:
#
#      SYYYYP,  where S = Season, YYYY = Year, P = Phase
#
#      examples:   S1901M, F1917B, F1911B
#
#      Note:  U = Summer, W = Winter
#
     if String[ 'Season' ] == 'Spring' :
          Temp = 'S'
     elif String[ 'Season' ] == 'Summer' :
          Temp = 'U'
     elif String[ 'Season' ] == 'Fall' :
          Temp = 'F'
     elif String[ 'Season' ] == 'Winter' :
          Temp = 'W'
     Temp = Temp + str( String[ 'Year' ] )
     if String[ 'Phase' ] == 'Moves' :
          Temp = Temp + 'M'
     elif String[ 'Phase' ] == 'Retreats' :
          Temp = Temp + 'R'
     elif String[ 'Phase' ] == 'Builds' :
          Temp = Temp + 'B'
     return Temp
     
def Game_Date_Sort_Value ( Game_Date ) :
#
# Converts a Game Date into a Sort Key, as follows:
#
#      Seasons:  Spring  <  Summer    <  Fall  <  Winter
#      Phases:   Moves   <  Retreats  <  Builds
#
     Temp = str( Game_Date[ 'Year' ] )
     if Game_Date[ 'Season' ] == 'Spring' :
          Temp = Temp + '1'
     elif Game_Date[ 'Season' ] == 'Summer' :
          Temp = Temp + '2'
     elif Game_Date[ 'Season' ] == 'Fall' :
          Temp = Temp + '3'
     elif Game_Date[ 'Season' ] == 'Winter' :
          Temp = Temp + '4'
     if Game_Date[ 'Phase' ] == 'Moves' :
          Temp = Temp + '1'
     elif Game_Date[ 'Phase' ] == 'Retreats' :
          Temp = Temp + '2'
     elif Game_Date[ 'Phase' ] == 'Builds' :
          Temp = Temp + '3'
     return Temp

def Add_Colon ( Text ) :
     return Text + ':'

def Read_Game ( File_Name, First_Date, Powers ) :
     Game_Start = {}
     Game_Finish = {}
     Game_Players = {}
     Game_Eliminees = {}
     Flag = 'start'
     File = open( File_Name )
     for Line in File.readlines() :
          if not Line : continue
          Line_Words = string.split( Line )
          if not Line_Words : continue
          if Flag == 'start' :
               if Line[ 0:16 ] == 'Summary of game ' :
                    Game_Name = Line_Words[ 3 ][ 1:-1 ]
                    Game_End_Date = Convert_String_to_Game_Date( Line_Words[ -1 ][ :-1 ] )
               elif Line_Words[ 0 ] in map( Add_Colon, [ 'Master' ] + Powers.keys() ) + [ 'from' ] :
                    if Line_Words[ 0 ] != 'from' :
                         Player_Power = Line_Words[ 0 ][ :-1 ]
                         Game_Players[ Player_Power ] = {}
                         Offset = 0
                         Date = First_Date
                    else :
                         Offset = 1
                         Date = Line_Words[ 1 ][ :-1 ]
                    Player_Name = Line_Words[ 1 + Offset ]
                    for Position in range( len( Line_Words ) - 3 - Offset ) :
                         Player_Name = Player_Name + ' ' + Line_Words[ Position + 2 + Offset ]
                    Player_EMail = Line_Words[ -1 ]
                    Game_Players[ Player_Power ][ Date ] = {}
                    Game_Players[ Player_Power ][ Date ][ 'Player' ] = Player_Name
                    Game_Players[ Player_Power ][ Date ][ 'EMail' ] = Player_EMail
               elif Line[ 0:36 ] == 'Game parameters are/were as follows:' :
                    Flag = 'parameters'
          elif Flag == 'parameters' :
               if Line_Words[ 0 ] == 'Press:' :
                    Game_Press = ''
                    if Line_Words[ 1 ] == 'None' :
                         Game_Press = 'None'
                    else :
                         if Line_Words[ 1 ] == 'White,' :
                              Game_Press = 'W-'
                         elif Line_Words[ 1 ] == 'Grey,' :
                              Game_Press = '-G'
                         elif Line_Words[ 1 ] == 'White/Grey,' :
                              Game_Press = 'WG'
                         if ( Line_Words[ 2 ] == 'No' ) and ( Line_Words[ 3 ] == 'Partial' ) :
                              Game_Press = Game_Press + '--'
                         elif Line_Words[ 2 ] == 'Partial' :
                              Game_Press = Game_Press + 'P'
                         elif ( Line_Words[ -2 ] == 'No' ) and ( Line_Words[ -1 ] == 'Fake.' ) :
                              Game_Press = Game_Press + '-'
                         else :
                              Game_Press = Game_Press + 'F'
               elif Line_Words[ 0 ] == 'Judge:' :
                    Judge_Name = Line_Words[ -1 ][ : -1 ]
               elif Line[ 0:14 ] == 'Game Started: ' :
                    Game_Start[ 'Year'  ] = Line_Words[ 6 ]
                    Game_Start[ 'Month' ] = Line_Words[ 3 ]
                    Game_Start[ 'Day'   ] = Line_Words[ 4 ]
                    Game_Start[ 'Time'  ] = Line_Words[ 5 ]
               elif ( Line[ 0:10 ] == 'Game won: ' ) or ( Line[ 0:15 ] == 'Draw declared: ' ) :
                    Game_Finish[ 'Year'  ] = Line_Words[ 6 ]
                    Game_Finish[ 'Month' ] = Line_Words[ 3 ]
                    Game_Finish[ 'Day'   ] = Line_Words[ 4 ]
                    Game_Finish[ 'Time'  ] = Line_Words[ 5 ]
                    Game_Winners = []
                    Flag = 'winners'
          elif Flag in [ 'winners', 'more winners' ] :
               if Line[ 0:20 ] == 'The game was won by ' :
                    Game_Winners = [ Line_Words[ 5 ][ :-1 ] ]
                    Flag = 'comment'
               else :
                    if Line[ 0:37 ] == 'The game was declared a draw between ' :
                         Offset = 7
                    elif Line[ 0:25 ] == 'The game was conceded to ' :
                         Offset = 5
                    else :
                         Offset = 0
                    Flag = 'more winners'
                    for Power in Line_Words[ Offset: ] :
                         if Power[ -1 ] in ',.' :
                              Game_Winners.append( Power[ :-1 ] )
                              if Power[ -1 ] in '.' :
                                   Flag = 'comment'
                         elif Power != 'and' :
                              Game_Winners.append( Power )
          elif Flag == 'comment' :
               if Line[ 0:32 ] == 'Historical Supply Center Summary' :
                    if Game_End_Date[ 'Season' ] == 'Spring' :
                         Last_SC_Year = Game_End_Date[ 'Year' ] - 1
                    else :
                         Last_SC_Year = Game_End_Date[ 'Year' ]
                    Flag = 'SCs'
          elif Flag in [ 'SCs', 'more SCs' ] :
               if Flag == 'SCs' :
                    if Line_Words[ 0 ] == First_Date[ 1:5 ] :
                         Flag = 'more SCs'
               else :
                    Temp = []
                    for Power in Powers.keys() :
                         if not ( Powers[ Power ][ 'Abbrev' ] in Line_Words ) :
                              Temp.append( Power )
                    for Power in Powers.keys() :
                         if not ( Game_Eliminees.has_key( Power ) ) and ( Power in Temp ) :
                              Game_Eliminees[ Power ] = {}
                              Game_Eliminees[ Power ] = Line_Words[ 0 ]
                    if Line_Words[ 0 ] == str( Last_SC_Year ) :
                         Flag = 'end'
     if Flag != 'end' :
          print
          print 'ERROR reading in the Judge Summary'
          print
          print 'Flag = %s' % Flag
          print
          print Game_Name
          print Game_End_Date
          print Game_Players
          print Game_Press
          print Judge_Name
          print Game_Start
          print Game_Finish
          print Game_Winners
          print Game_Eliminees
          exit
     File.close()
     return ( Judge_Name, Game_Name, Game_Press, Game_Start, Game_Finish, Game_End_Date, Game_Players, Game_Winners, Game_Eliminees )
