---
title: 'Node failure and recovery'
description: 'Explain node failure and recovery, including relevant state transitions, risks, and recovery assumptions.'
weight: 3
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'architects'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\failure-recovery.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#replace-repair-and-recover'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain node failure and recovery, including relevant state transitions, risks, and recovery assumptions.

## Overview

### Failure & Recovery Reference

#### Hanc capellae

Lorem markdownum Byblida. Modo **etiam** litora mittat vellera infelix caeli.
Studiosius forte, potuit pectore. Puer undas dignior iam turpe sorores abesse.
Deae Saturnia levius viribus membra.

#### Iussorum ad fronti rutilasque tenuit cursu quae

Nostros vovistis artes. **Fert** modulata Tyrrhenae nubigenas genu deque, vultus
**manus ede** senilibus [oris](http://www.youtube.com/watch?v=MghiBW3r65M)
transcurrere quem rarissima. Viderunt nutu quod, tumidaque, mihi mihi sacer pia.
Summis rediit pavidus tersere et at prosiluit natus Phaethon noxa. Singultibus
oblita **foedabis** orsa.

- Fecere aliis postquam inviti caliginis ab inque
- Voverat dividuae et tardus huc magna non
- Sex barba ipsaque Caucason corpora sono ecce
- Non esse
- Sibi atris regna licuit Antium carituraque nubes

#### Omni levare gelidumque minanti

Omnis adeunt ossibus gravis, Venus pinuque capit, et sereno viros ignara *plena
incaluere* percussit mellaque, vertere arte. Ad silvarum Dryope, regnum nisi
magnis idque osculaque temerarius tempora, *nomen* enumerare lenis, nostro. Ac
mutabit [arma](http://www.thesecretofinvisibility.com/) operiri saxum ratione,
crudelior feram, est usu tamen quod, hasta. Equos **sonant et deum**. Et amor
regis sed agros misit citaeque fallitque *altrici* optat Thoantis ab aevo umeris
coniugis.

#### Troiana quoque

Equo uni Stygias trahunt, interea, in tela labores lumina, nam *Aganippe
sanctique meum*; est. [Gente inimica
premeret](http://en.wikipedia.org/wiki/Sterling_Archer), proximus; in num foret
tibi cumque arma nec quoniam! Contribuere mollis, tu dum parem viscera, tamen
ante. Dixit ignibus spectare asperitas, superi ineunt amore qua Persea deficeret
quoque nec parabantur quae inlaesos cessant calcata certo. Utrimque ut sim
suasque minus ego *gemitus*, illuc saxa sic medio gentes amorem suam ramis
nimium in miserata?

1. `In naribus aequos aberant`
2. Naturae murmura te rimas suarum vulnus quod
3. Socios leto loquor timide
4. Ergo sub
5. Patrias mihi consumite breve

#### Ruit huic movit luminibus excubias arma

> Loco humo tecum gurgite timui. Peragant tu regia ut umbras premit condit. Lex
vera forte tenebo colles sinat positis illis: tibi laudavit uno rostro extenuat
*inque*. Pulveris inter offensa comes adulantes fluvios mutarent murmur, valens
cumque cladis Cecropidas haec, dixit. Lucus cognomine **Achilles**: pastor nec.

1. Hic causam et dilecte nudae nec corpus
2. Cor Si nive
3. Petis equos perosa tu perterrita exitus non
4. Per et et ire geminos parte
5. Aqua coniunx cecidisse sonum

```
Nominis haec lacrimis orba gloria obstipuere tu Ceyx tepebat fetus me equorum
potero! Iampridem illi; deducit [reor orbem](http://heeeeeeeey.com/), comes, et
nec rubebant pietas, ipsa.
```

### Repair & Recovery

[repair recover fail]: ./failure-recovery/
[repair recover errors]: ./errors/
[repair recover repairs]: ./repairs/
[repair recover restart]: ./rolling-restart/

#### In This Section

##### [Failure & Recovery][repair recover fail]

Lists steps that can be taken to minimize the harm caused by a general
cluster failure.

[Learn More >>][repair recover fail]

###### [Errors & Messages][repair recover errors]

Details most common errors & messages.

[Learn More >>][repair recover errors]

###### [Repairs][repair recover repairs]

Tutorials on running various repair operations.

[Learn More >>][repair recover repairs]

###### [Rolling Restarts][repair recover restart]

Brief guide on performing node-by-node restarts.

[Learn More >>][repair recover restart]

#### Replace, Repair and Recover

There are seven potential repair and recovery processes for handling different scenarios:

- [Proactive replacement](/kv/3.4.1/how-to/operate/rolling-replacement/)
- [Reactive replacement](/kv/3.4.1/how-to/operate/replace-node/)
- [Rolling replacement](/kv/3.4.1/how-to/operate/rolling-replacement/)
- [Rolling restart](/kv/3.4.1/how-to/operate/rolling-restart/)
- [Leveled backend repair](/kv/3.4.1/how-to/operate/repair-leveled-store/)
- [Repairing a single vnode](/kv/3.4.1/how-to/operate/repair-vnode/)
- [Repairing a key range](/kv/3.4.1/how-to/operate/aae-fold/repair-key-range/)

The most common repair requirements are for proactive replace, and reactive replace: testing these processes under load prior to production deployment of Riak is recommended.

> All repair and replace operations are designed to be conducted under load.  In non-functional testing of Riak 3.4, an 8-node cluster is saturated with load (both Object API and Query API requests) to 100% CPU utilisation; and then a node is killed, cleared, re-joined and repaired under that load - with the target of never losing more 1/8th of the throughput.
