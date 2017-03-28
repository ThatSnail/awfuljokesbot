# awfuljokesbot

![](/images/bargentina.png)
![](/images/octagondola.png)
![](/images/refunderpants.png)

Ohoho my sides!  Find more at [@AwfulJokesBot](https://twitter.com/AwfulJokesBot).

# How to run
Run

    python awfuljokes.py

to generate a joke!

# How it works
The joke restricts itself to the following form:

    What do you get when you cross a ____ with a ____? A ____!

First, the pun itself is generated.  The ARPABET list allows words to be mapped to their phonemes.  Two nouns are found where the last phonemes of one noun match the first phonemes of the other.  They are then combined together in a really Frankenstein-ish procedure that only really works about half of the time.

Then the nouns are searched for on Wikipedia and the most common words on their respective Wikipedia pages become candidates for the start of the joke.
