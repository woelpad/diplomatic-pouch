import check_variant

( M,O,T,P,C,S,H,U ) = check_variant.Select_Variant( 'Standard' )
check_variant.Check_Variant( M,O,T,P,C,S,H,U )



Names     = 'N'




Borders   = 'B'

Terrain = {	'Mountains' : [ ],
			'Lands'		: [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ],
			'Waters'	: [ ] }
			
Map1 = {	 0: { Names : [  '0' ], Borders : [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ] },
			 1: { Names : [  '1' ], Borders : [ 0, 2, 5 ] },
			 2: { Names : [  '2' ], Borders : [ 0, 1, 3 ] },
			 3: { Names : [  '3' ], Borders : [ 0, 2, 4, 6 ] },
			 4: { Names : [  '4' ], Borders : [ 0, 3, 5, 7, 8 ] },
			 5: { Names : [  '5' ], Borders : [ 0, 1, 4, 8, 9 ] },
			 6: { Names : [  '6' ], Borders : [ 0, 3, 7 ] },
			 7: { Names : [  '7' ], Borders : [ 0, 4, 6 ] },
			 8: { Names : [  '8' ], Borders : [ 0, 4, 5 ] },
			 9: { Names : [  '9' ], Borders : [ 0, 5 ] } }
			
Map2 = {	 0: { Names : [  '0' ], Borders : [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ] },
			 1: { Names : [  '1' ], Borders : [ 0, 2, 3, 4 ] },
			 2: { Names : [  '2' ], Borders : [ 0, 1, 4 ] },
			 3: { Names : [  '3' ], Borders : [ 0, 1, 4 ] },
			 4: { Names : [  '4' ], Borders : [ 0, 1, 2, 3, 5, 6 ] },
			 5: { Names : [  '5' ], Borders : [ 0, 4, 7 ] },
			 6: { Names : [  '6' ], Borders : [ 0, 4, 7 ] },
			 7: { Names : [  '7' ], Borders : [ 0, 5, 6, 8, 9, 10 ] },
			 8: { Names : [  '8' ], Borders : [ 0, 7, 10 ] },
			 9: { Names : [  '9' ], Borders : [ 0, 7, 10 ] },
			10: { Names : [ '10' ], Borders : [ 0, 7, 8, 9 ] } }
			