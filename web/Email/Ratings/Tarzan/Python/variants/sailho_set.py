#
# Sail Ho! Diplomacy Variant
#
# Initial Setup Positions
#
# The Units Dictionary is of the form 
#
#	key : Province Name     value : Dictionary of Unit Kind/Power
#
# The Unit Kind Dictionary is of the form 
#
#	key : Unit Kind (Army or Fleet)	value : Power Name
#

Start_Year   = 1901
Start_Season = 'Spring'
Start_Phase  = 'Moves'

Units = 	{	'Her' : { 'North' : 'Army'  },
			'Aeo' : { 'North' : 'Army'  },
			
			'Had' : { 'South' : 'Army'  },
			'Xen' : { 'South' : 'Fleet' },
			
			'Cen' : { 'East'  : 'Army'  },
			'Ama' : { 'East'  : 'Fleet' },
			
			'Les' : { 'West'  : 'Fleet' },
			'Ves' : { 'West'  : 'Fleet' }
		}
