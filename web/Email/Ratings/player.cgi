#!/home/dippouch/bin/python

from rating import *

print 'Content-type: text/html\n'

print """
<HTML>
<HEAD>
<TITLE>DP Email: Player Rating Details</TITLE>
</HEAD>

<BODY BGCOLOR="#ffffff">
<p align=center>
<A HREF="../..">
<IMG SRC="../../Common/DPLogo.gif"
ALT="The Diplomatic Pouch" HEIGHT=45 WIDTH=164 BORDER=0></A>
<A HREF="/cgi-bin/imagemap/DipPouch/Common/DPLinks.map">
<IMG SRC="../../Common/DPLinks.gif" ALT="Shortcuts"
HEIGHT=45 WIDTH=423 BORDER=0 ISMAP></A>
<br clear=all>
<img src="../../Common/reddot.gif" height=2 width=100%>
"""

form = cgi.FieldStorage()
if not form:
	print """
		<H1 align=center>Individual Player Data</H1>
		<center>
		<form action=player.cgi method=post>
		<b>E-Mail Address:</b>
		<input name=email size=30>
		<br>
		<input type=submit value="Show The Data">
		</form>
		"""
	email = 'manus@evolving.com'
	# raise SystemExit
email = string.lower(form['email'].value)
if form.has_key('system'):
	system = form['system'].value
	playerDir = '/home/dippouch/public_html/Email/Ratings/%s/players/' % system

player = {email: load(email, playerDir)}

if not player[email]:
	print """
	<H2 align=center><font color=red>
	No Record of Any Player With E-Mail Address<br>"%s"
	</font>
	<form>
	<input type=button value="Go Try Again" onclick=window.history.back()>
	</form>
	""" % email
	raise SystemExit

while type(player[email]) == type(''):
	email = player[email]
	player = {email: load(email, playerDir)}

print """
	<H1 align=center>Player Rating Details<br>%s</H1>
<center>
<table border cellpadding=2 cellspacing=2>
<tr><th><th>Game<th>Power<th>Started<th>Finished<th>Result<th>Points
""" % player[email][NAME]

games, count = player[email][GAME].keys(), 0
games.sort()
for game in games:
	if player[email][GAME][game][FINISH]: finish = 'YES'
	else: finish = 'NO'
	if player[email][GAME][game][ANTE]: start = 'YES'
	else: start = 'NO'
	if player[email][GAME][game][RESULT] == 0: result = 'loss'
	elif player[email][GAME][game][RESULT] == 1: result = 'solo'
	else: result = '%dway' % player[email][GAME][game][RESULT]
	count = count + 1
	print \
"""
<tr><td>%d.<td><tt><b>%s</b></tt>
	<td align=center>%s
	<td align=center>%s
	<td align=center>%s
	<td align=center>%s
	<td align=right>%.3f
""" % ( count, game,
		player[email][GAME][game][POWER], start, finish,
		result, player[email][GAME][game][SCORE] )

print ('<tr><th align=right colspan=6>Total:<td align=right>%.3f' %
	player[email][SCORE])
print '</table></center>'
print """
<P>
<img src="../../Common/reddot.gif" height=2 width=100%>
<H5>
<p align=center>
[       <a href="../../Zine">The Zine</a> |
        <a href="../../Online">Online Resources</a> |
        <a href="../../Showcase">Showcase</a> |
        <a href="../../Postal">Postal</a> |
        <a href=..>Email</a> |
        <a href="../../Face">Face to Face</a>
]
<br>
<i>The Diplomatic Pouch is brought to you by
<a href="../../Council.html">the DP Council</a>.
<br>
The Email Diplomacy section is maintained by <a href="mailto:masseyd@valhalla.btv.ibm.com">Doug Massey</a>.
<br>
The PBEM Ratings are maintained by <a href="mailto:Elladan@hotmail.com">Eric Hunter</a>.
</i>
"""

