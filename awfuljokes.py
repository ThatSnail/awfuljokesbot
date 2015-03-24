import string
import wikipedia
import re
import math
import random

VOWELS = "AEIOUYaeiouy"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXZbcdfghjklmnpqrstvwxz"
MIN_PHENOMES_SHARED = 3

def getPhenomes(word):
	word = word.upper();
	result = "Word not found."
	refFile = open("phoneme_ref.txt");
	for line in refFile.read().splitlines():
		if line.find(word, 0, len(word)) > -1:
			result = line
			break
	refFile.close();
	# clean result
	result = result[len(word)+1:]
	return result

def getWordAssocs(word, n):
	nounfile = open("nouns")
	nounlist = [x for x in nounfile.read().splitlines()]
	nounfile.close()

	wikitext = wikipedia.getArticle(word)
	wordlist = []
	if wikitext == False:
		return False
	for words in wikitext.split():
		words = words.lower()
		words = words.translate(string.maketrans("", ""), string.punctuation)
		if nounlist.count(words) > 0:
			if [x[1] for x in wordlist].count(words) == 0:
				wordlist.append((1, words))
			else:
				i = [x[1] for x in wordlist].index(words)
				t = wordlist[i] # tuple
				wordlist[i] = (t[0]+1, t[1])
	wordlist.sort()
	wordlist.reverse()
	return [x[1] for x in wordlist[:n]]

def getRandomNoun():
	nounfile = open("nouns")
	nounlist = [x for x in nounfile.read().splitlines()]
	nounfile.close()

	return nounlist[int(math.floor(random.random() * len(nounlist)))]

def badjoke():
	ASSOC_COUNT = 5	

	word1 = getRandomNoun()
	word2 = getRandomNoun()
	print("What do you get when you cross a " + word1 + " with a " + word2 + "?")

	wordassocslist1 = getWordAssocs(word1, ASSOC_COUNT)
	wordassocslist2 = getWordAssocs(word2, ASSOC_COUNT)

	if wordassocslist1 == False or wordassocslist2 == False or len(wordassocslist1) == 0 or len(wordassocslist2) == 0:
		print("JOKE FAILED, ABORT, ABORT")
		return

	print([getPhenomes(x) for x in wordassocslist1])
	print([getPhenomes(x) for x in wordassocslist2])
	
#	wordassocs1 = wordassocslist1[int(math.floor(random.random() * len(wordassocslist1)))]
#	wordassocs2 = wordassocslist2[int(math.floor(random.random() * len(wordassocslist2)))]

#	print("A " + wordassocs1 + wordassocs2)

def getNounPuns(list1, list2):
	punlist = []
	for word1 in list1: # word1 = "bowl"
		for word2 in list2: # word2 = "fishbowl"
			phenword1 = getPhenomes(word1) # phenword1 = ("B OW L")
			phenword2 = getPhenomes(word2) # phenword2 = ("F IH SH B OW L")
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
	if CONSONANTS.count(letter) > 0:
		return True
	else:
		return False

def isVowel(letter):
	if VOWELS.count(letter) > 0:
		return True
	else:
		return False

def getConsonantCount(word):
	consonantCount = 0
	for letter in list(word):
		if isConsonant(letter):
			consonantCount += 1
	return consonantCount

def pruneNoun(word, phonemes):
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
	if isVowel(word[0]):
		return "n " + word
	else:
		return " " + word

def main():
	result = ""
	while True:
		noun1 = getRandomNoun()
		noun2 = getRandomNoun()
		list1 = [noun1]
		list2 = [noun2]
		punlist = getNounPuns(list1, list2)
		if punlist != []:
			jokenoun1 = getWordAssocs(noun1, 1)[0]
			jokenoun2 = getWordAssocs(noun2, 1)[0]
			result += "What do you get when you cross a" + conjunctify(jokenoun1) + " with a" + conjunctify(jokenoun2) + "? "
			result += "A" + conjunctify(punlist[0]) + "!"
			break
	print(result)
main()
