#!/usr/bin/python -O

print 'Content-type: text/html\n'

##import cgi, os
##try: from data import data
##except: data = {}
##form = cgi.FieldStorage()
##answer = form.has_key('vote') and form['vote'].value or None
##if answer != None:
##	list = data.get(os.environ['REMOTE_ADDR'], [])
##	list.append(answer)
##	data[os.environ['REMOTE_ADDR']] = list
##	file = open('data.py', 'w')
##	file.write('data = %s\n' % `data`)
##	file.close()
##
print (
"""
<HEAD>
   <TITLE>DP F1999R: Paradox Resolution Rules</TITLE>
</HEAD>
<BODY bgcolor=white>
<A HREF="../.."><IMG align=left SRC="../../Common/DPbutton.gif" border=0></A>
<A HREF=".."><IMG align=right SRC="../../Common/toF1999R.gif" border=0></A>
<BR clear=both><HR>

<H1 align=center>Paradox Resolution Rules</H1>
<H2 align=center><i>By Simon Szykman and Manus Hand</i></h2>
<HR>
<H3>Thanks For Answering....</H3>
Okay, now for the rules and discussion.  Both Simon and Manus came up 
with different rules that would avoid the paradox in the scenario
described previously.  The first rule results in the first of the
two possible outcomes shown, and the second rule results in the second
of the outcomes show.  In case it isn't obvious, this is an either-or
situation.  Paradoxes would be eliminated by adding only one of the two
rules to the current rules.
<p>
<blockquote><i>
<b><font color=red>Paradox-eliminating Rule Number 1:</font>
"If a convoyed army attacks a fleet
that is supporting an action in or into a body of water that contains a
convoying fleet, that support is not cut by the convoyed army under
any circumstance (but a convoying army does cut all other supports
normally)."
<!--
"Even if a convoying army succeeds in dislodging the the fleet at its
destination location, it does not cut the support offered by that fleet,
if (and only if) that support for was an attack on a fleet that carried
the attacking army. Other than this single exception, the convoying army
cuts all other supports normally."
-->
</b></i>
<!--
"If a convoyed army attacks a fleet
that is supporting a fleet which is attacking one of the fleets convoying
that army, that support is not cut by the convoyed army <u>under any
circumstance</u> (but a convoying army does cut all other supports normally)."
-->
<p><i><b>
<font color=red>Paradox-eliminating Rule Number 2:</font> "If a situation arises in which an
army's convoy order results in a paradoxical adjudication, the turn is
adjudicated as if the convoying army had been ordered to hold."</b>
</i></blockquote>
<p>
In case you want to see the setup again, here is the initial setup
and the two outcomes:
<p>
<table cellpadding=5>
<tr><th>Original Situation
<th>Resolution Using Rule 1
<th>Resolution Using Rule 2
<tr><th rowspan=2><img src=paradox.gif>
<th valign=top><img src=rule1.gif>
<th valign=top><img src=rule2.gif>
<tr><td colspan=2>
<tt>F Wal - ENG<br>
    F Lon S F Wal - ENG
<p>A Bre - ENG - Lon<br> 
    F ENG C A Bre - Lon<br> 
    A Yor S A Bre - Lon
<p>F Bel - ENG<br>
    F NTH S F Bel - ENG 
</table>

<p>
Before moving on to the discussions, a couple of general points.
<ol>
<li><b>Neither one of these rules is in the Diplomacy rulebook.</b>
You will always
have purists who say that the official rules, albeit flawed, are the
ones that should be used.  There's not much to say to these 
purists.  Leaving the rules as they are now is not a big deal, since 
these paradoxical situations generally don't arise in your average game.
On the other hand, the current rules are <i>flawed</i> because they allow these
paradoxical situations -- cases in which there is no single adjudication
that is consistent with all the rules.  Therefore, if something <i>can</i>
be done to remedy those paradoxical situations, why not consider it?
<P>
<li>
<b>Both of the proposed rules are, in a way, inconsistent with
or contradictory to the rules that are already in the rulebook.</b>
In other words, the current rulebook consists of a set of rules that
allow certain
unusual cases to be irresolvable because the rules are not fully
consistent, and both of the proposed solutions are the result of adding to
the rulebook another rule that is not completely consistent with the
existing set of rules.
</ol>
<p>
So by way of a disclaimer, it should be noted that Simon and Manus do not
claim that their proposed solutions are consistent with the current
rulebook.  Their claim is that the rulebook is already flawed by 
inconsistencies that causes paradoxes, and that those paradoxes can be
eliminated by adding one of these proposed rules.  With or without the
paradox-eliminating rules, the rulebook includes consistencies.  So they
advocate an inconsistent set of rules where paradoxes have been eliminated
over an inconsistent set of rules that allows paradoxical situations.  And
these rules will only affect these rare situations where paradoxes arise...
they will not affect regular gameplay.
<p>
And with that, you can read the two discussions, one making a case for 
rule 1 over rule 2, and the other making a case for rule 2 over rule 1.
<p>
<center>
<table>
<tr>
<th>
<form method=get action=rule1.html>
<input type=submit value="Read the Argument For Rule 1">
</form>
<!--
<th>
<form method=get action=rule2.html>
<input type=submit value="Read the Argument For Rule 2">
</form>
</table>
</center>
<p>
<center>
<table>
<tr>
<th>
<form method=post action=finish.cgi>
<input type=hidden value=1 name=vote>
<input type=submit value="I Like Rule 1">
</form>
<th>
<form method=post action=finish.cgi>
<input type=hidden value=2 name=vote>
<input type=submit value="I Like Rule 2">
</form>
<th>
<form method=post action=finish.cgi>
<input type=hidden value=3 name=vote>
<input type=submit value="I Prefer the Current Situation">
</form>
<th>
<form method=post action=finish.cgi>
<input type=hidden value=0 name=vote>
<input type=submit value="I Can't Decide">
</form>
-->
</table>
</center>
After you have read the two discussions, you can vote again for
whichever you think is a better solution to the paradox situation.

<P>
<table>
<tr valign="bottom">
<td><A HREF="mailto:manus@manushand.com"><IMG src="../../Common/letter.gif" border="0"></A>
</td>
<td>
<strong>Manus Hand<br>
(manus@manushand.com)</strong>
</td>
</tr>
<tr valign="bottom">
<td><A HREF="mailto:simon@diplom.org"><IMG src="../../Common/letter.gif" border="0"></A>
</td>
<td>
<strong>Simon Szykman<br>
(simon@diplom.org)</strong>
</td>
</tr>
</table>
<p>
<i>If you wish to e-mail feedback on this article to the author, and clicking
on the envelope above does not work for you, feel free to use the
<A HREF="../Common/DearDP.html">
"<b>Dear DP...</b>"</A> mail interface.</i>
<p>
<HR>

<A HREF="../.."><IMG align=left SRC="../../Common/DPbutton.gif" border=0></A>
<A HREF=".."><IMG align=right SRC="../../Common/toF1999R.gif" border=0></A>
<BR clear=both>

</BODY>
</HTML>
""")
