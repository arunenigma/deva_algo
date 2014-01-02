# -*- coding: utf-8 -*-
from io import BytesIO

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from nltk import bigrams, trigrams, ngrams
from string import maketrans
from lxml import etree


class Corpus(object):
    def __init__(self, tweet, tweet_words, bi_grams, tri_grams, four_grams, five_grams):
        self.tweet = tweet
        self.tweet_words = tweet_words
        self.bi_grams = bi_grams
        self.tri_grams = tri_grams
        self.four_grams = four_grams
        self.five_grams = five_grams

    def parse_xml(self):
        #parser = etree.XMLParser(ns_clean=True, remove_pis=True, recover=True)
        parser = etree.XMLParser(recover=True)
        f = etree.parse(BytesIO(self.tweet), parser)
        fstring = etree.tostring(f, pretty_print=True)
        print fstring
        element = etree.fromstring(fstring)
        return element

    def generate_location_vector(self, branch, index):
        if branch.text is not None:
            branch.text = branch.text.encode('ascii', 'ignore')

            if not branch.getchildren():
                sentences = branch.text.split('. ')

                for sentence in range(0, len(sentences)):
                    #sentence_location = (("{0}[{1}]".format(index, sentence)), sentences[sentence])
                    words = sentences[sentence].split()

                    for word in range(0, len(words)):
                        word_location = (("{0}[{1}][{2}]".format(index, sentence, word)), words[word])
                        symbols = ",[]();:<>+=&+%!@#~?{}|"
                        whitespace = "                      "
                        replace = maketrans(symbols, whitespace)
                        tweet_word = word_location[1].translate(replace)
                        tweet_word = tweet_word.lstrip()
                        tweet_word = tweet_word.rstrip()

                        if len(tweet_word) > 1 and not len(tweet_word) > 16:
                            self.tweet_words.append(tweet_word)

                    bi_grams = bigrams(words)
                    if not len(bi_grams) < 1:
                        for bi_gram in bi_grams:
                            bi_gram = ' '.join(bi_gram)
                            self.bi_grams.append(bi_gram)

                    tri_grams = trigrams(words)
                    if not len(tri_grams) < 1:
                        for tri_gram in tri_grams:
                            tri_gram = ' '.join(tri_gram)
                            self.tri_grams.append(tri_gram)

                    four_grams = ngrams(words, 4)
                    if not len(four_grams) < 1:
                        for four_gram in four_grams:
                            four_gram = ' '.join(four_gram)
                            self.four_grams.append(four_gram)

                    five_grams = ngrams(words, 5)
                    if not len(five_grams) < 1:
                        for five_gram in five_grams:
                            five_gram = ' '.join(five_gram)
                            self.five_grams.append(five_gram)                    

            else:
                for subtree in range(0, len(branch)):
                    Corpus.generate_location_vector(self, branch[subtree], ("{0}[{1}]".format(index, subtree)))