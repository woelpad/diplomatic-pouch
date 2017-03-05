#!/home/dippouch/bin/python

import os, string, cgi, sys

# -----------------------------------------------
# Perform the assignments to gameCount and player
# -----------------------------------------------
from data import *

NAME, GAME, TURNS, ANTE, FINISH, SCORE, POWER, RESULT = range(8)

system = 'YARS2'

comdir = '/home/dippouch/public_html/Email/Ratings/data'
precision = 3

names = {}

def figureGame(fileName):
	if not names:
		for addr in player.keys():
			if type(player[addr]) != type(''):
				names[string.lower(player[addr][NAME])] = addr
	fileName = string.strip(fileName)
	print 'Figuring %s...' % fileName
	global gameCount
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
			addrs, guy = string.split(string.lower(email), ','), None
			# ---------------------------------------------
			# Check if e-mail is registered in database yet
			# ---------------------------------------------
			for addr in addrs:
				if player.has_key(addr):
					guy = addr
					while type(player[guy]) == type(''): guy = player[guy]
					if name and not player[guy][NAME]:
						names[string.lower(name)], player[guy][NAME] = guy, name
					break
			else:
				lowname = string.lower(name)
				if names.has_key(lowname): guy = names[lowname]
				else:
					# ----------------------
					# Add new e-mail address
					# ----------------------
					names[lowname] = guy = addrs[0]
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
					player[addr] = guy

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
			else: game[power][guy][SCORE] = -game[power][guy][ANTE]
			player[guy][ANTE] = player[guy][ANTE] + game[power][guy][ANTE]
			player[guy][FINISH] = player[guy][FINISH] + game[power][guy][FINISH]
			player[guy][SCORE] = player[guy][SCORE] + game[power][guy][SCORE]
			player[guy][GAME][gameName] = game[power][guy]

	gameCount = gameCount + 1

def save():
	file = open('data.py', 'w')
	file.write('gameCount = %d\n' % gameCount)
	file.write('player = %s\n' % `player`)
	file.close()
	os.chmod('data.py', 0666)

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
