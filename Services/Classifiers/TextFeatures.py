# -*- coding: utf-8 -*-
import itertools
import math
import nltk
import string
import re
from SuperGLU.Classifiers.ModelFeature import (ModelFeature, FeatureSelector,
    InSequenceFeature, OrderFeature)


# Features
#--------------------------------
class KeywordFeature(InSequenceFeature):
    NAME_PREFIX = 'KEYWORD_'

    def __call__(self, value):
        value = wordSplitFunction(value, stem=True)
        return super(KeywordFeature, self).__call__(value)

class WordOrderFeature(OrderFeature):
    NAME_PREFIX = 'WORD_ORDERING_'
    
    def __call__(self, value):
        value = wordSplitFunction(value, stem=True)
        return super(WordOrderFeature, self).__call__(value)

class VerbosityFeature(ModelFeature):
    NAME_PREFIX = 'Verbosity_'
    def __init__(self, name=NAME_PREFIX+'Log', transform=None):
        super(VerbosityFeature, self).__init__(self.NAME_PREFIX + name)
        if transform is None: transform = lambda x: math.log(x+1)
        self._transform = transform

    def __eq__(self, other):
        return (super(VerbosityFeature, self).__eq__(other) and
                self._transform == other._transform)

    def __call__(self, value):
        return self._transform(len(wordSplitFunction(value, stem=False)))

class NegationFeature(ModelFeature):
    NEGATION_TERMS = frozenset(['n', 'no', 'non', 'not', "n't"])
    
    def isNegation(self, word):
        return word in self.NEGATION_TERMS

class NegationCountFeature(NegationFeature):
    NAME_PREFIX = 'NegationCount'
    def __init__(self, name=NAME_PREFIX):
        super(NegationCountFeature, self).__init__(name)

    def __call__(self, value):
        return len([w for w in wordSplitFunction(value, stem=False) if self.isNegation(w)])

class NegationModFeature(NegationCountFeature):
    NAME_PREFIX = 'NegationMod'
    def __init__(self, name=NAME_PREFIX):
        super(NegationModFeature, self).__init__(name)
        
    def __call__(self, value):
        return super(NegationModFeature, self).__call__(value) % 2

# Feature Selectors
#--------------------------------
class KeywordExistenceSelector(FeatureSelector):
    def __init__(self, name, frequency=0, removeStopWords=True, wordFile='stopwords.txt'):
        super(KeywordExistenceSelector, self).__init__(name)
        self._frequency = frequency
        self._stopWords = self.getStopWords(wordFile, removeStopWords)

    def getStopWords(self, fileName, removeStopWords=True):
        if fileName is None or not removeStopWords:
            return set()
        stopWordsFile = open(fileName, 'r')
        stopWords = set([line.strip().lower() for line in stopWordsFile])
        return stopWords

    def calcWordFrequencies(self, classMap):
        classFreqs = dict([(aClass, {}) for aClass in classMap])
        for aClass, vals in classMap.items():
            for val in vals:
                words = [w for w in wordSplitFunction(val, stem=True)
                         if w not in self._stopWords]
                for word in words:
                    classFreqs[aClass][word] = classFreqs[aClass].get(word, 0) + 1
        for aClass, wordDict in classFreqs.items():
            total = len(classMap[aClass])
            for word, count in wordDict.items():
                classFreqs[aClass][word] = float(count)/total
        return classFreqs

    def getKeywordSetFromFreqs(self, classFreqs, frequency=None):
        if frequency is None: frequency = self._frequency
        words = set()
        for aClass, freqs in classFreqs.items():
            for word, freq in freqs.items():
                if freq >= frequency:
                    words.add(word)
        return sorted(list(words))

    def getKeywordList(self, inputs, outputs):
        classMap = self.binByOutput(inputs, outputs)
        freqs = self.calcWordFrequencies(classMap)
        words = self.getKeywordSetFromFreqs(freqs)
        return words
    
    def __call__(self, inputs, outputs, params=None):
        words = self.getKeywordList(inputs, outputs)
        features = [KeywordFeature(KeywordFeature.NAME_PREFIX + word, word) for word in words]
        return features

class WordOrderSelector(FeatureSelector):
    
    def __init__(self, name, words, minLength=2, maxLength=3, frequency=0.5):
        super(WordOrderSelector, self).__init__(name)
        self._words = set(words)
        self._minLength = minLength
        self._maxLength = maxLength
        self._frequency = frequency

    def getKeywordOrderFeatures(self, classMap):
        # Filter answers, then take orderings that exist
        orderings = dict([(aClass, {}) for aClass in classMap])
        kwds = self._words
        for aClass, cases in classMap.items():
            if len(kwds) > 1:
                for case in cases:
                    caseWords = [x for x in wordSplitFunction(case, stem=True) if x in kwds]
                    for i in xrange(self._minLength, self._maxLength+1):
                        for ordering in itertools.combinations(caseWords, i):
                            orderings[aClass][ordering] = orderings.get(ordering, 0) + 1
        for aClass, counts in orderings.items():
            total = sum(counts.values())
            for ordering in counts.keys():
                counts[ordering] = counts[ordering]/float(total)
                if counts[ordering] < self._frequency:
                    del counts[ordering]
        orderings = sorted(list(set(x for o in orderings.values() for x in o)))
        return orderings

    def __call__(self, inputs, outputs, params=None):
        classMap = self.binByOutput(inputs, outputs)
        orderings = self.getKeywordOrderFeatures(classMap)
        features = [WordOrderFeature(WordOrderFeature.NAME_PREFIX + str(ordering), ordering)
                    for i, ordering in enumerate(orderings)]
        return features

# Utility Functions
# Helper Functions
TOKENIZER = nltk.tokenize.treebank.TreebankWordTokenizer()
STEMMER = nltk.stem.porter.PorterStemmer()
REGEX_SPLITTER = re.compile("[^\w]")
MEMOIZE = {}
def wordSplitFunction(s, stem=False, fast=False):
    if s in MEMOIZE:
        return list(MEMOIZE[s])
    if fast:
        value = REGEX_SPLITTER.sub(" ",  s).split()
    else:
        tokens = TOKENIZER.tokenize(s)
        if stem:
            tokens = [STEMMER.stem(c) for c in tokens]
        else:
            tokens = [c.strip() for c in tokens]
        value= [c for c in tokens if (c not in string.punctuation and c != '')]
    MEMOIZE[s] = value
    return list(value)
