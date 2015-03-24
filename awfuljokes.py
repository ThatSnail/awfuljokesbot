import string
import wikipedia
import re
from math import floor
from random import random

VOWELS = "AEIOUYaeiouy"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXZbcdfghjklmnpqrstvwxz"
MIN_PHENOMES_SHARED = 2

class Words(object):
    """ A class for retrieving nouns and the like
    """
    def __init__(self):
        self.__nouns = []
        self.__phonemeDict = {}

    @property
    def nouns(self):
        if not self.__nouns:
            f = open("nouns")
            self.__nouns = f.read().splitlines()
            f.close()
        return self.__nouns

    def getRandomNoun(self):
        """ Return a random noun
        """
        return self.nouns[int(floor(random() * len(self.nouns)))]

    def phonemes(self, word):
        """ Given a word, return its phonemes
        """
        if not self.__phonemeDict:
            f = open("phoneme_ref.txt")
            self.__phonemeDict = {}
            for line in f.read().splitlines():
                k, v = line.split("\t")
                self.__phonemeDict[k.lower()] = v
            f.close()
        return self.__phonemeDict[word.lower()]

Words = Words()  # singleton

def getWordAssocs(word, n):
    """ Return the n most frequent nouns in the wiki article for 'word'
    """
    wikitext = wikipedia.getArticle(word)
    wordCounts = {}
    if wikitext == False:
        return False
    for word in wikitext.split():
        # Lowercase and remove punctuation
        word = word.lower()
        word = word.translate(string.maketrans("", ""), string.punctuation)

        if word in Words.nouns:
            if word not in wordCounts:
                wordCounts[word] = 1
            else:
                wordCounts[word] += 1
    # Return the n most frequent words
    items = [(v, k) for k, v in wordCounts.items()]
    items.sort()
    items.reverse()
    return [x[1] for x in items[:n]]

def getNounPuns(word1, word2):
    """ Given two nouns, return a list of puns
    """
    punlist = []
    try:
        phenword1 = Words.phonemes(word1) # phenword1 = ("B OW L")
        phenword2 = Words.phonemes(word2) # phenword2 = ("F IH SH B OW L")
    except KeyError:
        return []
    lword1 = phenword1.split() # lword1 = ("B", "OW", "L")
    lword2 = phenword2.split() # lword2 = ("F", "IH", "SH", "B", "OW", "L")

    # check prefixes word1, suffixes word2
    for phonemeCount in range(MIN_PHENOMES_SHARED, len(lword1) + 1): # phonemeCount = 2, 3
        newword = string.join(lword1[:phonemeCount]) # newword = "B OW"
        ind = string.find(phenword2, newword, 1)
        if ind != -1 and ind + len(newword) == len(phenword2):
            # pun found!
            punlist.append(word2 + pruneNoun(word1, newword))
    # check prefixes word2, suffixes word1
    for phonemeCount in range(MIN_PHENOMES_SHARED, len(lword2) + 1):
        newword = string.join(lword2[:phonemeCount])
        ind = string.find(phenword1, newword, 1)
        if ind != -1 and ind + len(newword) == len(phenword1):
            # pun found!
            punlist.append(word1 + pruneNoun(word2, newword))
    return punlist

def isConsonant(letter):
    return letter in CONSONANTS

def isVowel(letter):
    return letter in VOWELS

def getConsonantCount(word):
    return len(filter(isConsonant, list(word)))

def pruneNoun(word, phonemes):
    """ Cut the first syllable... sort of
    """
    phonemes.replace(" ", "")

    consonants = getConsonantCount(phonemes)

    consonantsCounted = 0
    cutindex = -1
    for letter in list(word):
        cutindex += 1
        if isConsonant(letter):
            consonantsCounted += 1
            if consonantsCounted >= consonants:
                break
    return word[cutindex:]

def conjunctify(word):
    """ Prefix 'n ' if the word starts with a vowel
    """
    if isVowel(word[0]):
        return "n " + word
    else:
        return " " + word

def makeJoke():
    joke = ""
    while True:
        noun1 = Words.getRandomNoun()
        noun2 = Words.getRandomNoun()
        punlist = getNounPuns(noun1, noun2)
        if punlist:
            jokenoun1 = getWordAssocs(noun1, 1)[0]
            jokenoun2 = getWordAssocs(noun2, 1)[0]
            joke += "What do you get when you cross a{0} with a{1}? ".format(conjunctify(jokenoun1), conjunctify(jokenoun2))
            joke += "A" + conjunctify(punlist[0]) + "!"
            break  # ... we're done here
    return joke

if __name__ == "__main__":
    print(makeJoke())
