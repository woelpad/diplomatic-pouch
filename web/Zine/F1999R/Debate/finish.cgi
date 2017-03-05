#!/home/dippouch/bin/python

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

print (
"""
<HEAD>
   <TITLE>DP F1999R: Paradox Resolved</TITLE>
</HEAD>
<BODY bgcolor=white>
<A HREF="../.."><IMG align=left SRC="../../Common/DPbutton.gif" border=0></A>
<A HREF=".."><IMG align=right SRC="../../Common/toF1999R.gif" border=0></A>
<BR clear=both><HR>

<H1 align=center>Paradox Resolved!</H1>
<H2 align=center><i>By Simon Szykman and Manus Hand</i></h2>
<HR>
<H3>Thanks Again!</H3>
Manus (who proposes rule 1) and Simon (who proposes rule 2) wish to 
thank you for your responses.  Simon also has a geeky postscript to
his proposal.  Feel free to <a href=postscript.html>read it here</a>
if you are interested in going off on a slight (yet related) tangent.
<P>
<blockquote>
<i>By the way, you can see Manus's rule in action (and yes, Simon's rule is
implemented too as an option called <tt>SAFE_CONVOYS</tt>) at the
<a href=../Hand/dpjudge.html>DPjudge</a>, the Pouch's Web-based Diplomacy
adjudicator that is unveiled elsewhere in this issue.
</i></blockquote>
<P>
<table>
<tr valign="bottom">
<td><A HREF="mailto:manus@diplom.org"><IMG src="../../Common/letter.gif" border="0"></A>
</td>
<td>
<strong>Manus Hand<br>
(manus@diplom.org)</strong>
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
