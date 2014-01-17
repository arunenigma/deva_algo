#!/usr/bin/env python
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
    def __init__(self, doc, doc_words, bi_grams, tri_grams, four_grams, five_grams):
        self.doc = doc
        self.doc_words = doc_words
        self.bi_grams = bi_grams
        self.tri_grams = tri_grams
        self.four_grams = four_grams
        self.five_grams = five_grams

    def parse_xml(self):
        #parser = etree.XMLParser(ns_clean=True, remove_pis=True, recover=True)
        parser = etree.XMLParser(recover=True)
        self.doc = '<xml>' + self.doc + '</xml>'
        f = etree.parse(BytesIO(self.doc), parser)  # self.doc must be xml
        fstring = etree.tostring(f, pretty_print=True)
        element = etree.fromstring(fstring)
        return element

    @staticmethod
    def n_gram_cleaner(n_grams):
        """
        n_grams is a list of tuples
        return: tuple with cleaned n_gram words
        """
        symbols = ".,[]();:<>+=&+%!@#~?{}|"
        whitespace = "                       "
        replace = maketrans(symbols, whitespace)

        cleaned_n_grams = []
        for n_gram in n_grams:
            cleaned_n_gram = []
            for word in n_gram:
                word = word.translate(replace)
                cleaned_n_gram.append(word)
            cleaned_n_grams.append(tuple(cleaned_n_gram))
        return cleaned_n_grams

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
                        symbols = ".,[]();:<>+=&+%!@#~?{}|"
                        whitespace = "                       "
                        replace = maketrans(symbols, whitespace)
                        doc_word = word_location[1].translate(replace)
                        doc_word = doc_word.strip()

                        if len(doc_word) > 1 and not len(doc_word) > 16:
                            self.doc_words.append(doc_word)

                    bi_grams = bigrams(words)
                    if not len(bi_grams) < 1:
                        bi_grams = self.n_gram_cleaner(bi_grams)
                        for bi_gram in bi_grams:
                            bi_gram = ' '.join(bi_gram)
                            self.bi_grams.append(bi_gram)

                    tri_grams = trigrams(words)
                    if not len(tri_grams) < 1:
                        tri_grams = self.n_gram_cleaner(tri_grams)
                        for tri_gram in tri_grams:
                            tri_gram = ' '.join(tri_gram)
                            self.tri_grams.append(tri_gram)

                    four_grams = ngrams(words, 4)
                    if not len(four_grams) < 1:
                        four_grams = self.n_gram_cleaner(four_grams)
                        for four_gram in four_grams:
                            four_gram = ' '.join(four_gram)
                            self.four_grams.append(four_gram)

                    five_grams = ngrams(words, 5)
                    if not len(five_grams) < 1:
                        five_grams = self.n_gram_cleaner(five_grams)
                        for five_gram in five_grams:
                            five_gram = ' '.join(five_gram)
                            self.five_grams.append(five_gram)                    

            else:
                for subtree in range(0, len(branch)):
                    Corpus.generate_location_vector(self, branch[subtree], ("{0}[{1}]".format(index, subtree)))