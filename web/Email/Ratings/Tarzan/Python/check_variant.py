#
#  Diplomacy Variant Defintitions and Subroutines
#
#  a Variant is specified as follows:
#
#       1.  the Game Map to be used
#       2.  the Supply Centers (SCs) on the Game Map
#       3.  the Powers in the Game
#       4.  the Home SCs for each Power
#       5.  the Starting Location for each Power's Units on the Game Map }
#




def Check_Map ( Map, OTB ) :
#
# checks each Province to ensure that:
#
#	1) alternative names for Provinces (e.g. "MAO", "Mid") are used ONLY once
#	2) NO Province is (accidently) named OTB (Off The Board)
#	3) each Border is actually on the Map
#	4) NO Province (accidently) borders itself
#	5) each Border is "2-way" (thus, if A 'Borders' B, then B 'Borders' A)
#
# Note that the SAME Border may be listed MORE THAN ONCE for a given Province.
# This is needed for multi-coast borders (e.g. Mid's border with Spa).
#
# A Lookup Table (which is a dictionary) of ALL possible names referencing the
# various Map Provinces (including "alternative" names) is returned.
#
	result = { }
	for Province in Map.keys() :
		for Alias in Map[ Province ][ 'Aliases' ] :
			if Alias == Province :
				print 'Error in Check_Map()'
				print( '"' + Alias + '" cannot be used as BOTH a Map Province name AND its own "alias".' )
				exit
			elif Alias in result.keys() :
				print 'Error in Check_Map()'
				print( '"' + Alias + '" cannot be used to name BOTH "' + result[ Alias ] + '" AND "' + Province + '".' )
				exit
			else :
				result[ Alias ] = Province
		result[ Province ] = Province
	for Province in Map.keys() :
		if Province == OTB :
			print 'Error in Check_Map()'
			print 'Illegal Province name, "%s".' % OTB
			exit
		else :
			for Border in Map[ Province ][ 'Borders' ] :
			     if Border != OTB :
					if not Map.has_key( Border ) : 
						print 'Error in Check_Map()'
						print( 'Map Province "' + Province + '" has Border Province "' + Border + '", which does NOT exist.' )
						exit
					elif Border == Province :
						print 'Error in Check_Map()'
						print( 'Map Province "' + Province + '" cannot Border itself.' )
						exit
					elif Province not in Map[ Border ][ 'Borders' ] :
						print 'Error in Check_Map()'
						print( 'One way Border between Map Provinces "' + Province + '" and "' + Border + '".' )
						exit
	return result


def Check_Terrain ( Map, Terrain ) :
#
# checks to ensure that:
#
#	1) the Terrain type is valid (i.e. "Lands", "Waters", "Mountains")
#	2) each Province listed as having a Terrain type is actually on the Map
#	3) each Map Province has EXACTLY 1 Terrain Type
#
	for Kind in Terrain.keys() :
		if Kind not in [ 'Lands', 'Waters', 'Mountains' ] :
			print 'Error in Check_Terrain()'
			print 'Unknown Terrain Type "' + Kind + '" specified.'
			exit
		for Province in Terrain[ Kind ] :
			if not Map.has_key( Province ) :
				print 'Error in Check_Terrain()'
				print 'Terrain Type specified for an unknown Map Province "' + Province + '".'
				exit
	for Province in Map.keys() :
		Count = 0
		for Kind in Terrain.keys() :
			Count = Count + Terrain[ Kind ].count( Province )
		if Count == 0 :
			print 'Error in Check_Terrain()'
		    	print( 'Map Province "' + Province + '" has NO specified Terrain Type.' )
		    	exit
		elif Count > 1 :
			print 'Error in Check_Terrain()'
			print( 'Map Province "' + Province + '" has MULTIPLE Terrain Types.' )
		    	exit

		    	
def Find_Province_Coasts ( Map, OTB, Terrain, Province ) :
#
# Returns a list of potential "coasts" for a designated Map Province.  These
# "coasts" are designated by the bordering Land and Water provinces.
#
	result = [ ]
	if Province in Terrain[ 'Lands' ] :
		Processing_Coast = 'false'
		Coast = [ ]
		for Border in Map[ Province ][ 'Borders' ] :
			if Border in Terrain[ 'Waters' ] :
				Processing_Coast = 'true'
				Coast.append( Border )
			else :
				if Processing_Coast == 'true' :
					Processing_Coast = 'false'
					result.append( Coast + [ Border ] )
				Coast = [ Border ]
		if Processing_Coast == 'true' :
			if Map[ Province ][ 'Borders' ][ 0 ] in Terrain[ 'Lands' ] :
				result.append( Coast + [ Map[ Province ][ 'Borders' ][ 0 ] ] )
			elif Map[ Province ][ 'Borders' ][ 0 ] in Terrain[ 'Waters' ] :
				if result == [ ] :
					result.append( Coast )
				else :
					result[ 0 ] = Coast + result[ 0 ]
			else :
				result.append( Coast )
		elif Map[ Province ][ 'Borders' ][ 0 ] in Terrain[ 'Waters' ] :
			result[ 0 ] = [ Map[ Province ][ 'Borders' ][ -1 ] ] + result[ 0 ]
		for Index in range( len( result ) ) :
			Count = result[ Index ].count( OTB )
			while Count > 0 :
				result[ Index ].remove( OTB )
				Count = Count - 1
	return result


def Find_Coasts ( Map, OTB, Terrain ) :
#
# Resolves conflicts over potential multi-coast Map Provinces.  The Map Creator
# has 2 options.  Either "merge" the multiple coasts into a single coastland, or
# name the individual coasts.
#
# I am beginning to add in Army/Fleet movement arrays here.  Not sure if this is 
# the place to do this or not.
#
	temp = { }
	for Province in Map.keys() :
		temp[ Province ] = { }
		temp[ Province ][ 'AMoves' ] = [ ]
		temp[ Province ][ 'FMoves' ] = [ ]
	for Province in Map.keys() :
		for Border in Map[ Province ][ 'Borders' ] :
			if ( Province in Terrain[ 'Lands' ] ) and ( Border in Terrain[ 'Lands' ] ) :
				temp[ Province ][ 'AMoves' ].append( Border )
			elif ( Province in Terrain[ 'Waters' ] ) and ( Border in Terrain[ 'Waters' ] ) :
				temp[ Province ][ 'FMoves' ].append( Border )
		Coasts = Find_Province_Coasts( Map, OTB, Terrain, Province )
		for Coast in Coasts :
			for Border in Coast :
				temp[ Province ][ 'FMoves' ].append( Border )
				temp[ Border ][ 'FMoves' ].append( Province )
	Multi_Coastal = [ ]
	for Province in Map.keys() :
		Coasts = Find_Province_Coasts( Map, OTB, Terrain, Province )
		if len( Coasts ) > 1 :
			print 'Map Province "' + Province + '" has Coasts:'
			for Coast in Coasts :
				print Coast
			print
			print 'For Map Province "' + Province + '" do you want to Merge the Coasts (1) or Name the SEPARATE Coasts (2)?'
			Value = input( '1. Merge  2. Name' )
			if Value == 2 :
				Multi_Coastal.append( Province )
				for Coast in Coasts :
					print Coast
					CID = input( 'Coast Name?   1. North  2. South  3. East  4. West' )
					CList = 'nsew'
					Coast_Name = Province + '/' + CList[ CID - 1 ] + 'c'
					temp[ Coast_Name ] = { }
					temp[ Coast_Name ][ 'AMoves' ] = [ ]
					temp[ Coast_Name ][ 'FMoves' ] = [ ]
					for Border in Coast :
						temp[ Coast_Name ][ 'FMoves' ].append( Border )
						temp[ Province ][ 'FMoves' ].remove( Border )
						temp[ Border ][ 'FMoves' ].append( Coast_Name )
						temp[ Border ][ 'FMoves' ].remove( Province )
#
#*** Tricky stuff here to ensure that ONLY the multi coast info gets done and not
#the regular coast stuff also watch out for Con which can be reached from BOTH
#of Bul's coasts
#***
#
	print 'multi-coast provinces are:  ',
	print Multi_Coastal
	return temp


def Check_Powers ( Powers, HTML_Background_Color ) :
#
# checks to ensure that:
#
#	1) the Power Names are used ONLY once
#	2) the Power Name Possessive forms (e.g. "English") are used ONLY once
#	3) the Power Name Abbreviations (e.g. "E") are used ONLY once
#	4) the Power HTML Colors (e.g. "#2200FF") are used ONLY once
#
# A Lookup Table (which is a dictionary) of ALL possible names referencing the
# various powers is returned.
#

	result = { }
	Abbreviations = { }
	Colors = { }
	Colors[ HTML_Background_Color ] = 'Background'
	for Power in Powers.keys() :
		result[ Power ] = Power
		Possessive_Name = Powers[ Power ][ 'Poss_Name' ]
		if result.has_key( Possessive_Name ) :
			print 'Error in Check_Powers()'
			print( '"' + Possessive_Name + '" cannot be used to Possessively Name BOTH "' + result[ Possessive_Name ] + '" AND "' + Power + '".' )
			exit
		else :
			result[ Possessive_Name ] = Power
		Abbrev = Powers[ Power ][ 'Abbrev' ]
		if Abbreviations.has_key( Abbrev ) :
			print 'Error in Check_Powers()'
			print( '"' + Abbrev + '" cannot be used to Abbreviate BOTH "' + Abbreviations[ Abbrev ] + '" AND "' + Power + '".' )
			exit
		else :
			Abbreviations[ Abbrev ] = Power
		Color = Powers[ Power ][ 'HTML_Color' ]
		if Color == HTML_Background_Color :
			print 'Error in Check_Powers()'
			print( '"' + Color + '" cannot be used as the HTML Color for BOTH the Background AND "' + Power + '".' )
			exit
		elif Colors.has_key( Color ) :
			print 'Error in Check_Powers()'
			print( '"' + Color + '" cannot be used as an HTML Color for BOTH "' + Colors[ Color ] + '" AND "' + Power + '".' )
			exit
		else :
			Colors[ Color ] = Power
	return result
	
def Check_SCs ( Province_Lookup_Table, Powers, SCs, Home_SCs ) :
#
# checks to ensure that:
#
#	1) each SC Province is actually on the Map
#	2) each Home SC has a valid Power
#	3) each Home SC Province is actually on the Map
#	4) each Home SC is actually a SC
#
# Note that MORE THAN ONE Power may have the SAME Home SC(s).  This can be used
# to designate builds on ANY SC (such as is used in the "Chaos" variant).
#
	for Province in SCs.keys() :
		if not Province_Lookup_Table.has_key( Province ) :
			print 'Error in Check_SCs()'
			print 'Unknown Map Province "' + Province + '" CANNOT be added as a SC.'
			exit
	for Power in Home_SCs.keys() :
		if not Powers.has_key( Power ) :
			print 'Error in Check_Home_SCs()'
			print( '"Unknown Power "' + Power + '" CANNOT be assigned Home SCs.' )
			exit
		else :
			for Province in Home_SCs[ Power ].keys() :
				if not Province_Lookup_Table.has_key( Province ) :
					print 'Error in Check_SCs()'
					print 'Unknown Map Province "' + Province + '" CANNOT be added as a Home SC for Power "' + Power + '".'
					exit
				elif not SCs.has_key( Province_Lookup_Table[ Province ] ) :
					print 'Error in Check_Home_SCs()'
					print 'Map Province "' + Province + '" is NOT a SC and cannot be a Home SC for Power "' + Power + '".'
					exit

def Check_Units_Setup ( Province_Lookup_Table, Powers, Units ) :
#
# checks to ensure that:
#
#	1) each Unit Province is actually on the Map
#	2) AT MOST ONE Unit is in each Map Province
#	2) each Unit is "owned" by a valid Power
#	3) each Unit has a valid "Type" (i.e. Army or Fleet)
#	4) each Unit is located in a Map Province with an "appropriate" Terrain
#	   (i.e. an Army on Land and a Fleet on Water or a "Coast")
#
# Note that a Unit MAY be positioned in ANY province (as long as the Terrain of
# the province is "appropriate").  This can even be used to place a unit in a
# NON-SC province.
#
	for Province in Units.keys() :
		if not Province_Lookup_Table.has_key( Province ) :
			print 'Error in Check_Units_Setup()'
			print( 'Unknown Map Province "' + Province + '" CANNOT have any Units located here.' )
			exit
		else :
			if len( Units[ Province ].keys() ) != 1 :
				print 'Error in Check_Units_Setup()'
				print( 'MULTIPLE Units specified for the SAME Map Province "' + Province + '".' )
				exit
			for Power in Units[ Province ].keys() :
				if not Powers.has_key( Power ) :
					print 'Error in Check_Units_Setup()'
					print( 'Unknown Power "' + Power + '" CANNOT have any Units on the Map.' )
					exit
				elif Units[ Province ][ Power ] == 'Army' :
					if not Map[ Province_Lookup_Table[ Province ] ].has_key( AMoves ) :
						print 'Error in Check_Units_Setup()'
						print 'Map Province "' + Province + '" CANNOT be occupied by an Army.'
						exit
				elif Units[ Province ][ Power ] == 'Fleet' :
					if not Map[ Map_Lookup_Table[ Province ] ].has_key( FMoves ) :
						print 'Error in Check_Units_Setup()'
						print 'Map Province "' + Province + '" CANNOT be occupied by a Fleet.'
						exit
				else :
					print 'Error in Check_Units_Setup()'
					print 'Unknown Unit Kind "' + Units[ Province ][ Power ] + '" CANNOT be added to Map Province "' + Province + '".'
					exit

def Select_Variant ( Variant ) :
	if Variant == 'Standard' :
		import variants.stnd_map
		import variants.stnd_ter
		import variants.stnd_pow
		import variants.stnd_scs
		import variants.stnd_hom
		import variants.stnd_set
		Map = variants.stnd_map.Map
		OTB = variants.stnd_map.OTB
		Terrain = variants.stnd_ter.Terrain
		Powers = variants.stnd_pow.Powers
		HTML_Background_Color = variants.stnd_pow.HTML_Background_Color
		SCs = variants.stnd_scs.SCs
		Home_SCs = variants.stnd_hom.Home_SCs
		Units = variants.stnd_set.Units
	elif Variant == 'Sail Ho!' :
		import variants.sailho_map
		import variants.sailho_ter
		import variants.sailho_pow
		import variants.sailho_scs
		import variants.sailho_hom
		import variants.sailho_set
		Map = variants.sailho_map.Map
		OTB = variants.sailho_map.OTB
		Terrain = variants.sailho_ter.Terrain
		Powers = variants.sailho_pow.Powers
		HTML_Background_Color = variants.sailho_pow.HTML_Background_Color
		SCs = variants.sailho_scs.SCs
		Home_SCs = variants.sailho_hom.Home_SCs
		Units = variants.sailho_set.Units
	elif Variant == 'Shift Left' :
		import variants.stnd_map
		import variants.stnd_ter
		import variants.stnd_pow
		import variants.stnd_scs
		import variants.stnd_hom
		import shiftl_set
		Map = variants.stnd_map.Map
		OTB = variants.stnd_map.OTB
		Terrain = variants.stnd_ter.Terrain
		Powers = variants.stnd_pow.Powers
		HTML_Background_Color = variants.stnd_pow.HTML_Background_Color
		SCs = variants.stnd_scs.SCs
		Home_SCs = variants.stnd_hom.Home_SCs
		Units = shiftl_set.Units
	elif Variant == 'Shift Right' :
		import variants.stnd_map
		import variants.stnd_ter
		import variants.stnd_pow
		import variants.stnd_scs
		import variants.stnd_hom
		import shiftr_set
		Map = variants.stnd_map.Map
		OTB = variants.stnd_map.OTB
		Terrain = variants.stnd_ter.Terrain
		Powers = variants.stnd_pow.Powers
		HTML_Background_Color = variants.stnd_pow.HTML_Background_Color
		SCs = variants.stnd_scs.SCs
		Home_SCs = variants.stnd_hom.Home_SCs
		Units = shiftr_set.Units
	return ( Map, OTB, Terrain, Powers, HTML_Background_Color, SCs, Home_SCs, Units )
	
def Check_Variant ( Map, OTB, Terrain, Powers, HTML_Background_Color, SCs, Home_SCs, Units ) :
	Province_Lookup_Table = Check_Map( Map, OTB )
	Check_Terrain( Map, Terrain )
	q = Find_Coasts ( Map, OTB, Terrain )
#	Coasts = Coast_Terrain_List( Map, Terrain )
	Powers_Lookup_Table = Check_Powers( Powers, HTML_Background_Color )
	Check_SCs( Province_Lookup_Table, Powers, SCs, Home_SCs )
	print 'Variant is OK'
	return q

def Coast_Terrain_List ( Map, Terrain ) :
#
# Returns a list of Map Provinces which qualify as "Coasts".  This list includes
# "Lands" and "Mountains" with at least one "Water" Border.
#
	result = [ ]
	for Province in Terrain[ 'Lands' ] + Terrain[ 'Mountains' ] :
		Coast = 'false'
		for Border in Map[ Province ][ 'Borders' ] :
			if Border in Terrain[ 'Waters' ] :
				result.append( Province )
				break
	return result

