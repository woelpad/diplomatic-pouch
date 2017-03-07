# Linguistic Harbingers of Betrayal

You just got a cable from Austria.  Typically he's long-winded, somewhat
obnoxious and stubborn... a high maintenance ally.  Now, however, he's
obliging, brief, and even pleasant.  You wonder if something is up and whether
you should protect your flank.  His language, although friendly on the
surface, might signify a future betrayal.

Changes in conversation patterns are a topic of interest to academic
researchers.  We (Vlad Niculae and Jordan Boyd-Graber) and our colleagues (Srijan Kumar and Cristian
Danescu-Niculescu-Mizil) took a shot at predicting betrayal from language
signals in Diplomacy.

## The Subtle Power of Language

Human language is an incredibly powerful communication device.
and people can accomplish much by wielding it well.  In Diplomacy,
making the right argument could constitute the difference between
victory and defeat.
But language is leaky!  The way we speak can unknowingly reveal a
great deal of underlying context and social information about the speaker.

Enabled by the availability of larger and larger online
discussion forums to study, scientists at the intersection of
statistical analysis, natural language processing and social
sciences have uncovered surprising ways in which language can
reveal things that the speaker might not intend, or even
attempt to hide.

Among many others, language has been found to reveal:

 * *[Whether an author is who she claims to
 be.](https://en.wikipedia.org/wiki/Stylometry)*  Even when trying
 to copy another's writing style, there are lower level patterns
 that the impersonator cannot easily hide nor mimic.  These are
 often frequencies of pronouns and other *empty* words.
 * *[What personality traits a speaker
 displays.](http://www.wwbp.org/personality-wc.html)* Studies have shown,
 for example, that *can't wait* is a more typically extraverted
 phrase, and *don't want to* is a sign of introversion in Facebook posts.
 * *[Whether expressed opinions are deceptive.](http://reviewskeptic.com/)* For
 example, fake positive hotel reviews are
 overly positive and use more first person pronouns.
 * *[Which way the balance of power leans in a
 conversation.](http://www.cs.cornell.edu/~cristian/Echoes_of_power.html)*
 People unintentionally copy phrase patterns when talking to
 someone they look up to.

Motivated by such precedents, we set out to study the linguistic
dynamics of lasting friendships.

## Sudden but Inevitable Betrayal

Even the closest of friendships sometimes break down
when one betrays for personal gain. Betrayal is a key dynamic in
Diplomacy, where good alliances can end with an act of backstabbing.
For this reason, the game provides an excellent platform for
capturing "organic" betrayal. (Asking people to fake it
in a lab wouldn't quite cut it.)

Therefore, we devised a way to find backstabbing in a collection of online
Diplomacy games.
From the moves that were ordered, it's easy to tell when players support
each other directly.  However, attacks can take many forms.  We used the following
rules to determine aggressive moves with high certainty. We consider that A attacks B if:

  * B is holding a territory that A moves into;
  * B moves into one of A's home supply centers;
  * B cuts A's support;
  * B and A are adjacent and move onto one another's locations (in this case, A also attacks B);
  * C does any of the above with B's support.

Of course, in Diplomacy there are more subtle ways to be aggresive towards someone, such
as not following up on a promise you made or not respecting a DMZ.  These cannot be easily
detected automatically, though, so we might be missing some attacks.
For this reason, we identify **strong alliances**: sequences of games
during which two players support each other repeatedly, frequently and
reciprocally.  In between such consistent supports, it's unlikely that there would
be non-explicit attacks that we miss.

**Betrayals** happen when, after such a fruitful friendship, one
of the players attacks the other.  We require that at least two detectable attacks
take place before declaring the couple to be at war.  This way, it's
unlikely that the attack was performed *for show*, to deceive another player.

These two sets of rules work well together to guarantee that we're looking
at actual betrayals.  The messages exchanged between players confirm this upon
manual inspection: the victims often react to betrayal with dismay
(*Well, that move was sour...*) and fake confidence (*Of course I saw that coming
a mile away!*).  However, we want to look at what happens *before*
betrayal takes place: any signals there would allow us to anticipate betrayal while
it's in the betrayer's best interest to hide it.  Since we can be certain about
supports, but we might not know all aggressive moves, we only look at the seasons
up to the final support in the sequence.
We performed statistical analysis on the conversation from 250 examples of unambiguous
betrayals, and 250 similar cases of solid friendships that are not followed by attacks
until the end of the game.

## Balance

There are conversation attributes that could reveal affective or
functional relationship dynamics, and we hoped these attributes would help
shine light on the nature of betrayal.  With this in mind, the
key things we counted are:

 - *The proportion of **positive sentiment** sentences in each message*.
 The positivity of messages can show how a player is feeling (or wants to
 appear to be feeling).
 - *The average **politeness** level of the requests a player makes in a message.*
 People think differently of others depending on how polite they are when asking
 for things.
 - *The average number of **planning** words.* These are words like
 *next* or *later*, and can reveal how the players think about the future of
 the relationship.

We found that balance is important. Betrayal happens in imbalanced
relationships, while, in the alliances that survive, both players communicate
with similar levels of positivity, politeness and planning.
The imbalance that precedes betrayal is not apparent far in advance, only a
few seasons before the treacherous act is committed.  

The figure below shows the change in the three attributes as
betrayal approaches.  In all three cases, when betrayal is far in the
future, the relationships appear balanced.  (Potentially, the plan to
betray hasn't been formed yet in most cases.)  Imbalance becomes
visible in terms of positivity (top) and planning (bottom):
the betrayer becomes very positive before the very end of the friendship,
while the victim gradually plans more and more a couple of seasons before.
In terms of politeness (middle), the victims are more likely to make less
polite requests several seasons before the end. Before the final support,
however, they are more polite, and it's the betrayers that become rude.

![Figure 1. Imbalance in alliances that break.  The horizontal axis shows the
number of seasons before the very final support order in the
alliance.  The vertical axes show the amount in which each feature is manifested.](betrayal.png)

## Thoughts

We designed our study in an attempt to find as much as possible
about the language of betrayal.  For this reason, we intentionally
avoided modeling many things that would likely make better predictors.
For instance, we didn't cover the cases where the people exchange
very few messages or none at all.  We didn't make use of the position
of the players' units, nor did we analyze what actual orders are discussed.
This gives our results the potential of holding in other scenarios of betrayal
outside of Diplomacy, although that would have to be tested.

Even so, with such rigorous constraints, the linguistic signal
managed to **predict betrayal** at a better-than-chance level.
An interesting challenge could be to combine this with
game-specific signals in a Diplomacy-playing AI.  From a more theoretical point
of view, we will attempt to widen the impact of these observations and find
similar dynamics in other types of long-term relationships.  An ambitious
parting question: would it be possible to pinpoint the very moment when
somebody plans a future betrayal?

*Our complete study and other information is available at [https://vene.ro/betrayal](https://vene.ro/betrayal).*
