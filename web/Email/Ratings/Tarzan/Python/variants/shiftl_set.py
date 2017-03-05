#
# Shift Left Diplomacy Variant
#
# Initial Setup Positions
#

# England	in Austrian	Home SCs
# Italy	in English	Home SCs
# Austria	in French	Home SCs
# Turkey	in German	Home SCs
# Russia	in Italian	Home SCs
# France	in Russian	Home SCs
# Germany	in Turkish	Home SCs

Army  = 'A'
Fleet = 'F'

Start_Year   = 1901
Start_Season = 'Spring'
Start_Phase  = 'Moves'

Units = 	{ 	'England' : [	( Army,  'Vie' ),
						( Army,  'Bud' ),
						( Fleet, 'Tri' ) ],
			'Italy' : 	[	( Fleet, 'Lon' ),
		  				( Fleet, 'Edi' ),
		  				( Army,  'Lvp' ) ],
			'Austria' : [	( Fleet, 'Bre' ),
		  				( Army,  'Par' ),
		  				( Army,  'Mar' ) ],
			'Turkey' : 	[	( Army,  'Mun' ),
		  				( Army,  'Ber' ),
		  				( Fleet, 'Kie' ) ],
			'Russia' : 	[	( Army,  'Rom' ),
		  				( Army,  'Ven' ),
		  				( Fleet, 'Nap' ) ],
			'France' : 	[	( Army,  'War' ),
		  				( Army,  'Mos' ),
		  				( Fleet, 'Sev' ),
		  				( Fleet, 'StP/sc' ) ],
			'Germany' : [	( Army,  'Smy' ),
		  				( Army,  'Con' ),
		  				( Fleet, 'Ank' ) ]
		}
