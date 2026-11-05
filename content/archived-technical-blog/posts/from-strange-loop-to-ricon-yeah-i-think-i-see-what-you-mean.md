---
title: "From Strange Loop to RICON: Yeah, I Think I See What You Mean"
date: "2015-10-13T11:59:27+00:00"
author: "Mark Allen"
original_url: "http://basho.com/posts/technical/from-strange-loop-to-ricon-yeah-i-think-i-see-what-you-mean/"
archive_url: "https://web.archive.org/web/20170801115356http://basho.com/posts/technical/from-strange-loop-to-ricon-yeah-i-think-i-see-what-you-mean/"
categories:
  - "Community & Events"
---
I’ve been thinking about Peter Alvaro’s talk “I See What You Mean” since attending this year’s [Strange Loop](http://www.thestrangeloop.com/) conference and I have a lot of say about it.

TL;DR is you should watch this talk and [discuss it with us at RICON](http://bit.ly/ricon15o):

It’s interesting to me that a significant number of talks in this year’s Strange Loop referenced a 1966 paper by [Peter Landin](https://en.wikipedia.org/wiki/Peter_Landin) called (somewhat tongue in cheek) [“The Next 700 Programming Languages.”](https://dl.acm.org/citation.cfm?id=365230.365257) In this paper, Landin describes a programming language which he says in a footnote might be aptly called “Church without the lambda” – but which in the paper is called “If You See What I Mean” (ISWIM).

Alvaro’s talk delved deeply into the question of “What is the semantics or meaning of a program?” Alvaro’s thesis is that the meaning of a program is to produce desired **outcomes** from a computing system but that current languages focus on provoking certain computer *behaviors*. In Alvaro’s view, this is backwards. This topic is covered in some detail in the Landin paper and it arises again and again.

In section 9 of the paper, Landin writes:

> An important distinction is the one between indicating what behavior, step-by-step, you want the machine to perform, and merely indicating what outcome you want.

In a few more paragraphs Landin continues with another thesis of Alvaro’s:

> It is a trivial and pointless task to rearrange some piece of symbolism into prefixed operators and heavy bracketing. It is an intellectually demanding activity to characterize some physical or logical system as a set of entities and functional relations among them. However, it may be less demanding and more revealing than characterizing the system by a conventional program, and it may serve the same purpose.

The idea being that the communication pattern used for human to computer communication may vary in form, with some forms being more suitable than others. In the middle part of Peter’s talk he establishes the unmistakable link between the program itself, the behaviors it causes and the outcomes that come almost as a side-effect of the behaviors.

Alvaro says this is messed up. We ought to be thinking about the **outcomes** and focus less on the program per se or the behaviors which induce the outcomes. He uses SQL as an example of how this might practically work. When you execute a query using SQL, you don’t write an explicit imperative procedure to answer the query. Rather you say, “this is the data I am interested in, and this is where it lives. You figure out how to make these propositions true (if it can be true given the facts contained in the system at this point in time.)”

Alvaro wondered, “Hey, is it possible to apply the semantics of a query language to building robust distributed systems?” but quite possibly in a more thorough and thoughtfully put way. So Alvaro (and other colleagues at UC Berkeley) built some experiments to play with this idea, and it turns out that it just might be possible to use a form a logical proposition to drive desired outcomes in distributed systems. He runs through several examples of this in his talk, some of them derived from the [Datalog language](http://docs.racket-lang.org/datalog/) and some examples with semantic modifications to Datalog such as the “[Dedalus](http://db.cs.berkeley.edu/papers/datalog2011-dedalus.pdf)” language Peter created.

One of the most interesting parts of the talk was the discussion of how state might be represented in a query language. He pointed out there’s a pretty strong notion of “time” in the system where state is partitioned into “past events” and “future events”. He says, as far as messages go, you can’t easily tell if a message has been received by a node, but you can track if a message was sent.

Another implication was that “knowledge is ephemeral.” It only has a semantic meaning in a specific time and a specific local node. He said that distributed computation is really the rendezvous of ephemera, where deduction can take place between facts which the system knows about at a particular time.

Alvaro started with the statement that “abstractions are dangerous.” He concluded:

- Respect your users by providing appropriate abstractions (they’re powerful tools, yo) because **you** are your users, too!
- Abstractions leak. Deal with it.
- And meaning well is better than “feeling good” In other words, programs aren’t about how programming makes a programmer feel per se. They’re about getting stuff done.
- Inventing languages is dope.

Some of the open questions I have – in Landin’s paper, he writes:

> …reduc[e] the extent to which the program conveys its information by explicit sequencing…

And by the use of a declarative query language, it seems that Peter is suggesting this is a desirable goal. He talks about how an optimizer decomposes a query into operations and sequences the operations correctly in a RDBMS. Presumably there would be an equivalent entity somewhere in the system. It isn’t clear to me how or if that can work well in complex distribution models. (Maybe that is future work?)

I am especially curious because given that knowledge only has meaning on a specific node and specific time, it seems like an optimizer in a declarative distributed system programming language would have to either: a) search a large space for lots of answers or b) have a pretty good idea of what nodes “know” what things before it tried to decompose the query into steps of operations. Also it seems like the sequence of things like map and reduce across sets of knowledge have pretty specific orderings if one desires the asked for outcomes – i.e., those operations are not commutative. Is that an “implementation detail?” Because it seems like a pretty hard problem to solve, especially if you’re seeking confluent operations which permit weak orderings between messages.

Peter recently tweeted that [John Backus’](http://amturing.acm.org/award_winners/backus_0703524.cfm) Turing award speech [Can Programming Be Liberated from the von Neumann Style? A Functional Style and Its Algebra of Programs](http://dl.acm.org/ft_gateway.cfm?id=1283933&type=pdf) was one of his favorite papers and I’m just now grappling with why that is. I liked it when I first read it because it was pretty clear to me that Backus felt like much (all?) the work he had put into FORTRAN was in some ways a failure. I now perceive that Peter likes it because it challenges readers to try and concieve of a model of computation which is dramatically different from what has come before – a model like what Peter sketches in this Strange Loop talk. Quoting the Backus paper:

> [T]here is a desperate need for a powerful methodology to help us think about programs, and no conventional language even begins to meet that need. In fact, conventional languages create unnecessary confusion in the way we think about programs.

As you read through Backus, it’s hard not to see that paper as a direct descendant of the Landin paper above. Indeed, a (different) Landin paper is included in the citations of the Backus paper. What makes that quote especially poignant to me is that it was written in 1977; almost 40 years ago. Given that, are we finally on the cusp of a big idea which will let us answer Backus’s question affirmatively?

Peter and I have been [discussing this further](https://gist.github.com/mrallen1/902ab46bedce96db9ba0) and I welcome your thoughts. We will both [be at RICON 2015](http://bit.ly/ricon15o ) where I’ll be speaking on the early history of distributed systems [on Thursday](http://ricon.io/agenda/). I’d love to have you there.

Let’s dig further into the future (and past) of programming languages.

[Mark Allen](https://twitter.com/bytemeorg)
