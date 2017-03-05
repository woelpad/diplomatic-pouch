
from cgi import FieldStorage
from string import split, upper, whitespace, letters, lower

def header(title, preface = 'DP'):
	print 'Content-type: text/html'
	print \
	"""
		<HTML>
		<TITLE>%s: %s</TITLE><BODY BGCOLOR="#ffffff">
		<p align=center><A HREF="/DipPouch">
		<IMG SRC="/DipPouch/Common/DPLogo.gif"
		ALT="The Diplomatic Pouch" HEIGHT=45 WIDTH=164 BORDER=0></A>
		<A HREF="/cgi-bin/imagemap/DipPouch/Common/DPLinks.map">
		<IMG SRC="/DipPouch/Common/DPLinks.gif" ALT="Shortcuts"
		HEIGHT=45 WIDTH=423 BORDER=0 ISMAP></A>
		<br clear=both><HR><H1 align=center>%s</H1>
	""" % (preface, title, title)

def footer():
	print \
	"""
		<hr><H5 align=center>
		[	<a href="/DipPouch/Zine">The Zine</a> |
			<a href="/DipPouch/Online">Online Resources</a> |
			<a href="/DipPouch/Showcase">Showcase</a> |
			<a href="/DipPouch/Postal">Postal</a> |
			<a href="/DipPouch/Email">Email</a> |
			<a href="/DipPouch/Face">Face to Face</a>
		]<br><i>The Diplomatic Pouch is brought to you by
		<a href="/DipPouch/Council.html">the DP Council</a>.
	"""

def validEmail(email):
	return (email and ' ' not in email and "'" not in email
		and list(email).count('@') == 1
		and email[0] != '@' and '.' in split(email, '@')[1]
		and split(email, '@')[1][0] != '.'
		and len(split(email, '.')[-1]) in [2,3])

