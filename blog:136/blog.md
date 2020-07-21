# Coordination Problems in Evolution: The Rise of Eukaryotes

### Introduction

This is a series of posts about coordination problems, as they appear in the course of biological evolution. It is based on the book "[The Major Transitions in Evolution](https://www.amazon.com/Major-Transitions-Evolution-Maynard-Smith/dp/019850294X)" by John Maynard Smith and Eörs Szathmáry. Previous part, discussing Eigen's paradox as well as the origin of chromosomes, can be found [here](http://250bpm.com/blog:135).

In this part we are going to look at the origin of eukaryotic cell, specifically at its acquisition of endosymbiotic organelles, and at the origin of multicellularity.

### Prokaryota vs. eukryota

While all single-celled organisms may look like similar wiggly little creatures to us, there is a huge difference between [prokaryota](https://en.wikipedia.org/wiki/Prokaryote) (like bacteria) and [eukaryota](https://en.wikipedia.org/wiki/Eukaryote) (like protozoa or, for that matter, our own cells). The cell wall is different. The interior of the cell is different. One has rigid cell wall, in the other it's the cytoskeleton that holds the cell together. One has a single-origin DNA strand attached to the cell wall, the other has nucleus containing chromosomes. One has mitochondria and chloroplasts, the other does not. Even the mechanism of cell division is different. If we haven't known that we share part of the genome, it would be easy to make a mistake and believe that the life on Earth had originated at two separate occasions.

The transition from prokayotes to eukaryotes is likely the most complex transition in the entire course of evolution. It took two billion years to happen. More than the emergence of life itself.

All that being said, we are going to look only at a single part of the evolution of eukaryotes, namely at their acquisition of mitochondria. Mitochondria were free-living cells once. But then they've became an inseparable part of eukaryotic cell. Hence, back to the coordination problems!

How did it come to be that some cells started living within other cells? Well, assuming that flexible cell wall and [phagocytosis](https://en.wikipedia.org/wiki/Phagocytosis) evolved before the domestication of mitochondria, getting them inside wouldn't be a big problem. It happens each time one cell eats another.

What's more interesting is how did the guest cell survive and how did the cooperative behavior between the host and the guest evolve.

### Symbiosis

Let's make a digression and think about [symbiosis](https://en.wikipedia.org/wiki/Symbiosis) for a second. If we assume that there are only two strategies for the host (cultivate the symbiont or try to kill it) and two strategies for the symbiont (cooperate with the host or parasitize) then the problem gets reduced to variants of the [prisoner's dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma) game.

Consider this kind of arrangement of payoffs. The numbers specify the fitness of the host (left) and the symbiont (right):

Host / Symbiont

cooperate

parasitize

cultivate

20 / 20

5 / 30

kill

15 / 0

**10 / 5**

It can be easily seen that there is only one equilibrium: Whatever the host does it's better for the symbiont to parasitize. And if the symbiont is a parasite it's always better for the host to kill it.

Under what conditions do we see this kind of game? The authors point out that this happens when **each individual host acquires some genetically different symbionts from the environment**. The reason is that it doesn't pay for the symbiont to invest in the cooperation with the host if the host is going to be killed by a different symbiont anyway.

How about a different scenario?

Host / Symbiont

cooperate

parasitize

cultivate

**20 / 20**

5 / 10

kill

15 / 0

**10 / 5**

The ideal strategy for the symbiont is not clear in this case. If the host is cultivator it may pay to the symbiont to cooperate. If, on the other hand, the host tries to kill it, the best thing for the symbiont to do would be to multiply as fast as possible, regardless to any damage to the host.

This kind of setup is expected **if each host acquires only a single symbiont from the environment**:

> However, with hosts infected by a single symbiont, cooperative mutualism is likely to be stable once it evolves. The evolution from parasitism to mutualism will be favored if the hosts killing response is ineffective, and if the further spread of the symbiont is greater if the host does survive. It will not occur if the host can rapidly rid itself of the parasite, or if the parasite spreads only by killing the host.

Finally, let's have a look at the the following scenario:

Host / Symbiont

cooperate

parasitize

cultivate

**20 / 20**

5 / 10

kill

15 / 15

10 / 0

Again, there's only one equilibrium. It's always better for the symbiont to cooperate and once it's cooperating, it's better for the host to cultivate it.

This happens when **the host acquires one or a few symbionts from one of its parents**.

It makes sense: If the only place you can disperse to are your host's children you really don't want to kill it.

So there's a rule of thumb emerging here: If the transmission of the symbiont happens between unrelated individuals (horizontal transmission) the symbiosis will evolve towards parasitism. If the symbiont is passed only from one parent to its children, then the relationship will evolve towards mutualism.

In fact, both experiments and observations in the wild show that vertical transmission of the symbiont leads to mutualism and horizontal transmission leads to parasitsm. There are some exceptions though. For example, the transmission of luminous bacteria in deep-see fish is horizontal, yet the symbionts are essential to the survival of their hosts.

### Parasites or livestock?

Now, let's get back to the origin of eukaryotic cell. What was the relationship between the early host cells and early mitochondria?

It may have been that the mitochondria were parasites. Maybe they sometimes escaped the host cell and infected different cells. However, the authors hint at an interesting alternative: The host cells may have farmed the mitochondria for the later consumption, just like we do with the cattle.

One important point to understand here is that, however we feel about slaughtering cows, from the population generics point of view it's a mutually beneficial arrangement. Homo Sapiens gets steaks. Bos Taurus becomes one of the most common terrestrial vertebrates around.

So, the host cells may have first consumed mitochondria, but then learned to keep them around (or rather inside) so that they can be consumed later.

And we do see some evidence that the host cell adopts active measures to keep the relationship mutualistic. In sexually reproducing species the transmission of mitochondria happens from one parent only. When human egg merges with human sperm, all the mitochondria from the sperm are discarded and only those from the egg make their way into the embryo. That, according to the model described above, prevents competition between the different strains of mitochondria at the expense of the host cell.

Later on in the evolution, straightforward consumption of the symbionts must have been replaced by protein "taps" that we see installed into the cell wall of mitochondria today. The taps allow the nutrients produced by the mitochondria to flow into the host cell. Think of Maasai puncturing the flesh of a cow and drinking the blood without killing the animal. The fact that the tap protein is always encoded in the DNA of the host cell rather than in mitochondrial DNA is a hint that the idea of the host cells "farming" mitochondria may not be that implausible.

### Gene transfer to the nucleus

Once the mitochondria were living inside the host cell a curious process began. The genes from the mitochondria started "jumping" into the host cell's nucleus.

By losing their genes, mitochondria lost the chance to break free from the eukaryotic cell for good. So why did it happen? And who benefited?

I really like this process because it shows how complex the interplay between different levels of selection can be. In particular, we have to do with three distinct levels of selection here: Selection on the level of the host cell, selection on the level of mitochondria and selection on the level of a single mitochondrial gene.

First, we can imagine a mitochondrial gene getting attached to a nuclear chromosome. It would be clearly advantageous for the gene: One more copy! Hooray! What's not to like?

But why didn't the gene got discarded from the nuclear DNA given that it performed no useful function? Well, it turns out that nuclear DNA can contain humungous amounts of [dead code](https://en.wikipedia.org/wiki/Non-coding_DNA) and yet the code doesn't get discarded by natural selection. Contrast that with prokaryotes which tend to keep their genetic code short, sweet and streamlined.

But wait. The gene would still be translated into protein. That would be a useless expenditure of energy and thus it would be selected against. To make it advantageous for the cell there must have been a mechanism to transport the protein back into mitochondria. Luckily, all that is needed for that is to add to the protein a "transit peptide", a handle which would be recognized by a receptor in the mitochondrial membrane and used to carry the protein inside. Creating such a handle is easy. [Baker & Schatz](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC304819/pdf/pnas00275-0045.pdf) pasted randomly chosen pieces of E. coli and mouse DNA in front of protein genes, and found that 2.7 per cent of the bacterial inserts and 5 per cent of the mammalian ones were successful transit peptides.

Another hint that the transition may be easy is that there is no distinct pattern to the transit peptides. In other words, the transit peptides probably evolved 700 times independently — once for each mitochondrial gene that was transferred into the nucleus.

When the gene is in nucleus and the peptide handle in its place, the mitochondria can gain advantage by discarding the genes that they don't need anymore (they are importing those proteins from the outside anyway). And, as already mentioned, prokaryotes are very good at stripping their genome of any unnecessary baggage. [Nick Lane](https://en.wikipedia.org/wiki/Nick_Lane) does some [back-of-the-envolope calculations](https://youtu.be/gaXhkZoOOYc?t=2307) and concludes that the energy savings are truly huge.

All of that being the case, the question is rather why all the genes haven't been transferred to the nucleus.

### Why the gene transfer stopped

For mitochondria, the process was stopped by the change in mitochondrial genetic code (see only kind-of-related but fun-to-read [column](http://www.cs.uml.edu/~kim/580/SA_genetic_code.pdf) by Douglas Hofstadter). As soon as one of the mitochondrial [codons](https://en.wikipedia.org/wiki/DNA_codon_table) began coding for a different amino acid, the genes could no longer jump to the nucleus. When they did they were turned into defective proteins by the old, unmodified nuclear translation machinery.

But that can't be the entire story. The chloroplast genes are encoded in the plain old generic code. Yet the [chloroplasts](https://en.wikipedia.org/wiki/Chloroplast) still keep some of the genes for themselves. This may (or may not) indicate that there's still some level of separate identity to the organelles, that they may have goals of their own not fully aligned with the goals of the enclosing eukaryotic cell. An example of that would be, for example, mitochondria trying to distort the sex ratio of the host species.

(As a side note, there are organelles called [peroxisomes](https://en.wikipedia.org/wiki/Peroxisome) that were once thought to be endosymbionts, very much like mitochondria. Except that they had no genes at all. It has been suggested that they may be endosymbionts that have transferred all of their genes to the nucleus. However, that idea has been recently [challenged](https://en.wikipedia.org/wiki/Peroxisome#Evolutionary_origins).)

### Multicullular life and Orgel's second rule

Multicellular life sure looks like it has a coordination problem. All those billions and trillions of cells have to cooperate somehow. Most of them have to give up individual reproduction and rather work for the benefit of all. Hell, there's even [programmed cell death](https://en.wikipedia.org/wiki/Programmed_cell_death) where the cell is expected to willingly die when there's no use for it any more.

But when you take a step back the argument doesn't make sense. All those cells are genetically identical. There aren't multiple entities engaging in a coordination problem. There's just one entity: The multi-cellular organism itself.

Or is there?

It may be instructive to pause here for a while and do an exercise in evolutionary thinking.

Consider what happens if a [somatic cell](https://en.wikipedia.org/wiki/Somatic_cell) mutates.

The mutation may cause the cell to divide in unregulated manner.

But there's even more intriguing possibility: Imagine that a the cell mutates in such a way that it's more likely to give rise to a [germ cell](https://en.wikipedia.org/wiki/Germ_cell). For example, a plant cell that would otherwise produce a leaf would give rise to a flower instead. By doing so it would lower the overall fitness of the organism: The plant would now have less leaves than what's optimal. However, at the same time the renegade cell would increase its own fitness because any pollen or seed produced by that flower would carry the mutated gene instead of the original one.

So what do you think? Does the above make sense or does it not? Is it really an intra-organism conflict? Think about that. I'll wait.

…

Smith and Szathmáry approach the problem by splitting it into two parts.

First, they discuss whether mutation that increases a chance of giving rise to a gamete creates an internal conflict and, consequently, selection pressure for other cells to evolve a mechanism to prevent such mutations. They conclude that it doesn't. After all, this is not much different from when the mutation occurs in a germ cell. The child will be slightly genetically different from the parent, but that's just how evolution works. If the child happens to be more fit than the parent, it will eventually prevail in the competition on the organism level. If not so, the new strain will be eliminated by the natural selection.

The second part of the question is what happens if the mutant is malignant, i.e. if it causes unregulated cell proliferation. We call that cancer. In that case, the authors conclude, there will be an actual selective force to prevent, or delay, the malignancy.

Have you got that right? If not so, don't be disappointed and think about [Orgel's second rule](https://en.wikipedia.org/wiki/Orgel%27s_rules). The rule says: "Evolution is cleverer than you are."

If you want to remember just one thing about evolution, Orgel's second rule may be a good choice.

In fact, Smith and Szathmáry, as good evolutionary biologists, have the rule ingrained and conclude the section by hedging their bets:

> There is, therefore, no reason to think that \[specific mechanisms discussed in the book\] evolved to suppress cell-cell competition. But the question is important, and we do not regard our arguments as decisive.

### To be continued

In the following parts I will cover the origin of sex and of social species. In the end I am going to speculate about possible parallels between coordination problems in evolution and coordination problems in human society.

**October 14th, 2018**