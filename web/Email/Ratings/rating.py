#!/home/dippouch/bin/python

import os, string, cgi, sys

# --------------------------------------------------------
# Perform the assignments to gameCount, scores, and player
# --------------------------------------------------------
from gamecount import *
player = {}

NAME, GAME, TURNS, ANTE, FINISH, SCORE, POWER, RESULT, CHEAT = range(9)

sysList = ['YARS', 'YARS2']

system =  ['YARS', 'YARS2']

comdir = '/home/dippouch/public_html/Email/Ratings/data'
playerDir = '/home/dippouch/public_html/Email/Ratings/%s/players/' % system

precision = 3

def fixEmail(email):
	while '/' in email:
		where = string.find(email, '/')
		email = email[:where] + '_' + email[where + 1:]
	return email

def load(fileName = None, playerDir = None):
	player = {}
	if fileName:
		fileName = fixEmail(fileName)
		if (os.path.exists(playerDir + fileName[0] + os.sep + fileName)):
			execfile(playerDir + fileName[0] + os.sep + fileName)
			return player.get(fileName, None)
	return None

def figureGame(fileName):
	global gameCount
	fileName = string.strip(fileName)
	print 'Figuring %s...' % fileName
	game, power, going, file, drawing = {}, None, 0, open(fileName), 0

	# -------------------------------------
	# Go thru the summary file line by line
	# -------------------------------------
	for line in file.readlines():
		if not line: continue
		word = string.split(line)
		if not word: continue

		# -------------------------------------
		# Determine number of turns in the game
		# -------------------------------------
		if word[0] == 'Summary':
			gameName = word[3][1:-1]
			gamelength, going = (string.atoi(word[-1][1:5]) - 1900) * 2, 1
			# -------------------------------
			# (adjust if Fall was not played)
			# -------------------------------
			if word[-1][0] == 'S': gamelength = gamelength - 1
		elif not going: continue
		elif word[0] == 'Judge:':
			gameName = gameName + ' (' + word[1][:-1] + ')'

		# ------------------------------------------
		# Determine power and number of turns played
		# ------------------------------------------
		elif word[0] in ['Austria:', 'England:', 'France:', 'Germany:',
			'Italy:', 'Russia:', 'Turkey:', 'from']:
			if word[0] != 'from': power, turns = word[0][:-1], gamelength
			elif not power: continue
			else:
				# ------------------
				# Replacement player
				# ------------------
				turns = (string.atoi(word[1][1:5]) - 1901) * 2
				season = word[1][0] + word[1][-2]
				if season in ['SR', 'FM']: turns = turns + 1
				elif season != 'SM': turns = turns + 2
				turns = gamelength - turns
				# -----------------------------------
				# Adjust play-time of previous player
				# -----------------------------------
				game[power][guy][TURNS] = game[power][guy][TURNS] - turns
				game[power][guy][FINISH] = 0

			# ----------------------------------
			# Handle Name and E-Mail Address(es)
			# ----------------------------------
			name, email = string.join(word[1 + (word[0]=='from'):-1]), word[-1]
			if not email:
				print 'BAD DATA IN GAME FILE %s' % fileName
				continue
			addrs, guy = string.split(string.lower(fixEmail(email)), ','), None
			# ---------------------------------------------
			# Check if e-mail is registered in database yet
			# ---------------------------------------------
			for addr in addrs:
				if addr == 'cheater': continue
				if player.has_key(addr):
					guy = addr
					while type(player[guy]) == type(''): guy = player[guy]
					break
				elif os.path.exists(playerDir + addr[0] + os.sep + addr):
					execfile(playerDir + addr[0] + os.sep + addr)
					while type(player[addr]) == type(''):
						addr = player[addr]
						execfile(playerDir + addr[0] + os.sep + addr)
					guy = addr
					if len(name) > len(player[guy][NAME]):
						player[guy][NAME] = name
				else:
					# ----------------------
					# Add new e-mail address
					# ----------------------
					guy = addrs[0]
					player[guy] = { NAME: name, ANTE: 0, FINISH: 0,
									SCORE: 0, GAME: {} }
				# ----------------------------
				# Add other e-mails as aliases
				# ----------------------------
				for addr in addrs:
					if not player.has_key(addr): player[addr] = guy
					elif addr != guy and type(player[addr]) != type(''):
						for gname in player[addr][GAME].keys():
							player[guy][GAME][gname] = player[addr][GAME][gname]
							player[guy][ANTE] = (player[guy][ANTE] +
								player[guy][GAME][gname][ANTE])
							player[guy][SCORE] = (player[guy][SCORE] +
								player[guy][GAME][gname][SCORE])
							player[guy][FINISH] = (player[guy][FINISH] +
								player[guy][GAME][gname][FINISH])
						# scores[guy] = (player[guy][SCORE], player[guy][NAME])
						# if addr in scores.keys(): del scores[addr]
						player[addr] = guy
			if 'cheater' in addrs: player[guy][CHEAT] = 1

			# -------------------------
			# Update data for this game
			# -------------------------
			if not game.has_key(power): game[power] = {}
			if not game[power].has_key(guy):
				game[power][guy] = {	ANTE: word[0] != 'from', FINISH: 1,
										SCORE: 0, TURNS: turns, POWER: power,
										RESULT: 0 }
			else:
				game[power][guy][FINISH] = 1
				game[power][guy][TURNS] = game[power][guy][TURNS] + turns

		# ---------------------------------------------
		# Determine list of point gainers for this game
		# ---------------------------------------------
		elif drawing or (len(word) > 3 and word[3] in ['won', 'declared']):
			if drawing: which = 0
			else: drawers, which = [], 5 + (2 * (word[3] == 'declared'))
			for guy in word[which:]:
				if guy[-1] in ',.': drawers.append(guy[:-1])
				elif guy != 'and': drawers.append(guy)
			drawing = (word[-1][-1] != '.')
			if not drawing:
				# -------------------------------
				# Determine point award per power
				# -------------------------------
				result = len(drawers)
				if system == 'YARS': payback = (8.0 - result) / result
				elif system == 'YARS2': payback = (7.0 - result) / result

	if system == 'MJH':
		points = pot = 0
		for power in game.keys():
			for guy in game[power].keys():
				#	--------------------------------------------------------
				#	In the MJH system, all original players of a power ante
				#	to a total of 100 points for the pot.  The ante value is
				#	determined by the percentage success (non-elimination)
				#	rate of a power as determined by raw data of all judge
				#	games rated as of 30 December 1998.  Note, however,
				#	that if a player cannot afford his power's ante, he does
				#	NOT pay it (the 100 point pot will be short).
				#	--------------------------------------------------------
				if game[power][guy][ANTE]:
					ante = {'Austria': 13, 'England': 15, 'France': 18,
							'Germany': 14, 'Italy': 12, 'Russia': 12,
							'Turkey': 16 }
					if player[guy][SCORE] > ante[power]:
						game[power][guy][SCORE] = -ante[power]
						pot = pot + ante[power]
				else: game[power][guy][SCORE] = 0
				#	--------------------------------------------------------
				#	In the MJH system, the rating points of the players are
				#	added up.  For powers played by multiple players, their
				#	ratings are included in proportion to turns played.
				#	--------------------------------------------------------
				points = points + player[guy][SCORE] * game[power][guy][TURNS]
		points = points / float(gamelength)
		for power in game.keys():
			for guy in game[power].keys():
				#	------------------------------------------------------
				#	All players also risk a percentage of the game result
				#	pot, which is (115 - 15 * numDrawers) points.  The
				#	percentage that each player risks is their own current
				#	ranking's proportion to the total of all player's
				#	rankings (with replacement players handled on a time-
				#	played basis).  Again, if a player cannot afford to
				#	pay his percentage, it is not paid and the pot is
				#	short for this game.
				#	------------------------------------------------------
				risk = ((player[guy].get(SCORE, 1000) / float(points)) *
						(115 - 15 * len(drawers)) *
						(game[power][guy][TURNS] / float(gamelength)))
				if player[guy][SCORE] > risk:
					game[power][guy][SCORE] = game[power][guy][SCORE] - risk
					pot = pot + risk
		#	-------------------------------------------------------------
		#	The total pot will be divided evenly among the drawing powers
		#	-------------------------------------------------------------
		payback = pot / len(drawers)
			
	# ---------------------------------
	# Add points to master ratings list
	# ---------------------------------
	for power in game.keys():
		for guy in game[power].keys():
			if game[power][guy].has_key(SCORE) and game[power][guy][SCORE]:
				player[guy][SCORE] = player[guy][SCORE]-game[power][guy][SCORE]
			share = payback * (game[power][guy][TURNS] / float(gamelength))
			if power in drawers:
				game[power][guy][RESULT] = len(drawers)
				if system == 'YARS':
					if game[power][guy][ANTE]: game[power][guy][SCORE] = share-1
					else: game[power][guy][SCORE] = max(0,min(share,payback-1))
				elif system == 'YARS2': game[power][guy][SCORE] = share
				elif system == 'MJH':
					game[power][guy][SCORE] = game[power][guy][SCORE] + share
			else:
				if system[:4] == 'YARS':
					game[power][guy][SCORE] = -game[power][guy][ANTE]
			if player[guy][GAME].has_key(gameName):
				del player[guy][GAME][gameName]
				player[guy][ANTE] = 0
				player[guy][FINISH] = 0
				player[guy][SCORE] = 0.0
				for oldGame in player[guy][GAME].keys():
					player[guy][ANTE] = \
						(player[guy][ANTE] + player[guy][GAME][oldGame][ANTE])
					player[guy][FINISH] = \
						(player[guy][FINISH]+player[guy][GAME][oldGame][FINISH])
					player[guy][SCORE] = \
						(player[guy][SCORE] + player[guy][GAME][oldGame][SCORE])
			player[guy][ANTE] = player[guy][ANTE] + game[power][guy][ANTE]
			player[guy][FINISH] = player[guy][FINISH] + game[power][guy][FINISH]
			player[guy][SCORE] = player[guy][SCORE] + game[power][guy][SCORE]
			player[guy][GAME][gameName] = game[power][guy]
	save()
	gameCount = gameCount + 1
	save(1)

def save(scorelist = 0):
	global player
	if not scorelist:
		# print 'Saving player data . . . .'
		print 'keys are: %s' % `player.keys()`
		for addr in player.keys():
#			print 'addr is:', addr
			if not addr or type(addr) != type(''):
				print 'BAD ADDRESS FOR player array[<<%s>>]' % addr
				continue
			if not os.path.isdir(playerDir + addr[0]):
				os.mkdir(playerDir + addr[0])
				os.chmod(playerDir + addr[0], 0777)
			# print 'Saving to', (playerDir + addr[0] + os.sep + addr)
			file = open(playerDir + addr[0] + os.sep + addr, 'w')
			file.write('player[%s] = %s\n' % (`addr`, `player[addr]`))
			file.close()
			os.chmod(playerDir + addr[0] + os.sep + addr, 0666)
		player = {}
	else:
		# print 'Saving score list data . . . .'
		file = open('gamecount.py', 'w')
		file.write('gameCount = %d\n' % gameCount)
		file.close()
		os.chmod('gamecount.py', 0666)

# ----------------------------------
# Stores a game coming off sys.stdin
# ----------------------------------
def storeGame():
	fileName = file = good = reading = None
	list = []
	for line in sys.stdin.readlines():
		word = string.split(line)
		if not word: continue
		if len(word) > 1 and word[0] == 'Judge:':
			judge = word[1][:-1]
			if not os.path.isdir(comdir + os.sep + judge):
				os.system('mkdir %s' % (comdir + os.sep + judge))
			fileName = comdir + os.sep + judge + os.sep + game
		elif line[:10] == 'Summary of': game, reading = word[3][1:-1], 1
		if reading:
			if word[-1] == 'someone@somewhere':
				if not os.path.isdir(comdir + '/../notRevealed/' + judge):
					os.system('mkdir ' + comdir + '/../notRevealed/' + judge)
				fileName = comdir + '/../notRevealed/' + judge + os.sep + game
			if (len(word) > 1
			and word[0] == 'Variant:' and word[1][:8] != 'Standard'): break
			list.append(line)
			if (line[:28] == 'The game was declared a draw'
			or	line[:16] == 'The game was won'):
				good = 1
			if good and word[-1][-1] == '.': break
	if good and not os.path.exists(fileName):
		file = open(fileName, 'w')
		for line in list: file.write(line)
		file.close()
		os.chmod(fileName, 0644)
	if type(fileName) != type(''):
		print 'Bad type for figureGame! (%s)' % fileName
	else:
		for sysName in sysList:
			system = sysName
			playerDir = '/home/dippouch/public_html/Email/Ratings/%s/players/' \
				% system
			figureGame(fileName)
