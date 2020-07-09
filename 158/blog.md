# Partying over Internet: Technological Aspects

Now, with billion people locked down in their homes, social contact over Internet becomes an increasingly important topic. Not only it allows people to stay in touch, it also lowers the incentives to [leave one's home and meet people in person](https://www.theguardian.com/world/2020/apr/04/uks-covid-19-lockdown-could-crumble-as-frustration-grows-police-warn) and thus contributes to the public health.

I threw an online birthday party few days ago and in this article I would like to share some of my observations about how a party over Internet differs from one in the physical world and point out some implications and possible improvements for videoconferencing software.

To start with, existing videoconferencing software is geared towards business meetings. And the differences between a business meeting and a party are easy to spot: At a party, there's much less structure. While at a meeting it's typically just one person that speaks and everybody else listens, at a party people tend to speak in parallel. At a party, non-verbal communication (facial expressions, gestures) is crucial. At a business meeting, not so much. At a meeting one wants to maintain self-control. At a party, one often rather wants to get rid of it. And so on and so forth.

So, let's move directly to my observations:

### Everyone should be visible

Unlike with Google Hangouts where the person speaking is displayed in full-screen view and everyone else as a small icon on the side, at a party a want to see everyone in parallel. Sometimes, it's someone's non-verbal accompaniment of someone else's speech that's the real fun. But even when that's not the case, I still want to follow how everyone reacts to what is being said, whether they are laughing, paying attention, not paying attention, preparing a snack, drinking, smoking or whether they have left for a moment, leaving just a lonely chair visible in the window.

In short, I want to see all the participants of the party, side by side, all of them in equally sized windows. Size of the window is too expensive a piece of psychological real estate to waste on such an obvious thing as "who's speaking at the moment". More about that below.

### Looking at people

Maybe the most unpleasant part of social videoconferencing is not being able to follow who's looking at whom. Everyone just stares, indiscriminately, at the camera.

I have no idea of how reliably the existing eye-tracking software works. After browsing the web for a minute it seems that eye tracking is used mostly for… optimizing ads??? What a waste of resources!

Anyway, it doesn't matter. Whether the software uses webcam to trace your gaze or whether you use mouse to explicitly point to whomever you are looking at the implications are more or less the same: First, I want the window I am looking at to get larger. Second, I want the person on the other side to know that I am looking at them - not necessarily in any obtrusive manner, I just want them to be aware of it, presumably by making my image slightly larger.

To give a practical example: One of the participants at the party wears an amusing mask. I point to the corresponding window which makes it larger and allows me to inspect the details of the mask. The person in question sees that I am looking at them and that, possibly, others are looking as well. They may choose to react to that.

Taken together, one would see large image of the person they are looking at, somewhat smaller images of people looking at them and small images of everyone else. That, I think, more of less reflects how people perceive each other in real-world social interactions.

### Eye contact

If I look and someone and that person looks back at me, that's a powerful social signal and it should be reflected by the software. For example, in such a case we could get a special communication channel, where not only we see each other in large windows but also the talk by other people can be muffled so that we can hear each other well. (By the way, this protocol of looking and looking back is based on "[cabeceo](https://www.verytangostore.com/cabeceo.html)" as practiced when dancing tango: You can invite a person to dance with you by looking at them and they may accept by looking back or refuse by looking away.)

In this post I am not going to speak about larger parties but the problem there is obvious: With many people present there are going to be many parallel conversations, resulting it too much noise and not being able to hear each other properly. Clearly, some kind of fluent separation of the party into subgroups is needed. And while this seems to be a hard problem, the eye contact protocol described above can be used at least as a starting point: Cabeceo protocol allows to create groups of two people. Can it be somehow generalized for groups of three or more?

### Kissing

In many cultures, kissing is an important part of social interaction. However, it doesn't lend itself well to communication over Internet.

Skype allows you to send an emoticon (e.g. a symbol of a heart) to your counterpart. But that doesn't really convey that feel of intimacy that the real kiss does. After all, emoticons were invented to be a substitute for non-verbal communication in the situations where people don't see each other (SMS, email) which makes them, in the context of videoconferencing, redundant at best and embarrassing at worst.

Obviously, sending a kiss through video can't be solved by purely technical means. It would require some social innovation. If Eskimos can kiss by rubbing their noses, why can't we devise a special Internet kiss? But if we do, the experience can be greatly improved by the software.

Consider the cabeceo protocol above. What if a kiss worked like this: I look at the other person. The other person looks at me. Our windows get larger, everyone else fades into background. Surrounding noises are muffled. Then we both touch cameras with our noses.

It would have to be tested in practice, but it kind of looks like it could feel quite intimate.

### More social signals

In the physical world there are many more ways to send social signals.

Consider, for example, the seating order. If I sit next to someone it may mean that I want to speak with them, or I may want to signal that I belong to a certain subgroup or maybe it was just the only empty chair left. (Note that many social signals are weak and ambiguous. But that's a feature, not a bug!)

Now, I've used seating order just as an example. Not everything that exists at a physical party has to be necessarily mimicked in an online party. However, if the developers of the videoconferencing software decide that seating order is worth mimicking, then it has implications for the product design. For example, ordering of windows on the screen would have to be the same for everyone. It can't be that you can rearrange them arbitrarily. Should sitting next to someone else come with some extras? Maybe I can whisper to a person sitting besides me. Etc.

### Miscellaneous

*   There's a natural worry that seeing only people's faces is going to prevent a lot of non-verbal communication (gestures). However, my anecdotal evidence is that people, especially as the party progresses, subconsciously tend to move away from the camera making their entire upper body visible and thus improving non-verbal communication channels.

*   Partying online is not all downsides. One upside is that, being at home, people have all kind of inventory at their disposal, which, at a meatspace party, they don't. In our case we've used a [plague mask](https://en.wikipedia.org/wiki/Plague_doctor_costume#/media/File:Medico_peste.jpg), a [peacock feather](https://images-na.ssl-images-amazon.com/images/I/91uTc7G0PoL.jpg), a [bandana](https://www.quien.net/wp-content/uploads/politica-quien-es/Subcomandante-Marcos.jpg). There may be no technological implications, but I think the behavior is worth mentioning anyway.

*   It's unclear whether you should see yourself among the participants of the party. On one hand, seeing yourself leads to more self-control, which is not that desirable at a party. On the other hand, people do like the feature and would probably feel awkward if it was removed. Feedback from a friend: "If I am not on the screen it would feel like I am not present at the party."

### Conclusion

These are just some random thoughts that I'm giving free to anyone who fancies to implement them. However, if you do, please do let me know! It would be really interesting to see how this works in practice.

**April 5th, 2020**