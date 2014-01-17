# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2014, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

# doc_analyzer.py generates input data for fuzzification

from nltk import word_tokenize, pos_tag, bigrams, trigrams, ngrams, corpus
from string import maketrans
from io import BytesIO
from lxml import etree
from math import log10
import enchant
import re


class LocationVector(object):
    def __init__(self, individual_doc, words, doc_bigrams, doc_trigrams, doc_fourgrams, doc_fivegrams):
        self.doc = individual_doc
        self.doc_words = words
        self.bi_grams = doc_bigrams
        self.tri_grams = doc_trigrams
        self.four_grams = doc_fourgrams
        self.five_grams = doc_fivegrams

    def parse_xml(self):
        #parser = etree.XMLParser(ns_clean=True, remove_pis=True, recover=True)
        parser = etree.XMLParser(recover=True)
        self.doc = '<xml>' + self.doc + '</xml>'
        f = etree.parse(BytesIO(self.doc), parser)
        fstring = etree.tostring(f, pretty_print=True)
        element = etree.fromstring(fstring)
        return element

    @staticmethod
    def n_gram_cleaner(n_grams):
        """
        n_gram is a tuple
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

                    for doc_word in range(0, len(words)):
                        word_location = (("{0}[{1}][{2}]".format(index, sentence, doc_word)), words[doc_word])
                        # any change in line below should be replicated in corpus.py also
                        symbols = ".,[]();:<>+=&+%!@#~?{}|"
                        whitespace = "                       "
                        replace = maketrans(symbols, whitespace)
                        doc_word = word_location[1].translate(replace)
                        doc_word = doc_word.lstrip()
                        doc_word = doc_word.rstrip()
                        if len(doc_word) > 1 and not len(doc_word) > 16:
                            self.doc_words.append(doc_word)

                    doc_bigrams = bigrams(words)
                    if not len(doc_bigrams) < 1:
                        doc_bigrams = self.n_gram_cleaner(doc_bigrams)
                        for bi_gram in doc_bigrams:
                            bi_gram = ' '.join(bi_gram)
                            self.bi_grams.append(bi_gram)

                    doc_trigrams = trigrams(words)
                    if not len(doc_trigrams) < 1:
                        doc_trigrams = self.n_gram_cleaner(doc_trigrams)
                        for tri_gram in doc_trigrams:
                            tri_gram = ' '.join(tri_gram)
                            self.tri_grams.append(tri_gram)

                    doc_fourgrams = ngrams(words, 4)
                    if not len(doc_fourgrams) < 1:
                        doc_fourgrams = self.n_gram_cleaner(doc_fourgrams)
                        for four_gram in doc_fourgrams:
                            four_gram = ' '.join(four_gram)
                            self.four_grams.append(four_gram)

                    doc_fivegrams = ngrams(words, 5)
                    if not len(doc_fivegrams) < 1:
                        doc_fivegrams = self.n_gram_cleaner(doc_fivegrams)
                        for five_gram in doc_fivegrams:
                            five_gram = ' '.join(five_gram)
                            self.five_grams.append(five_gram)

            else:
                for subtree in range(0, len(branch)):
                    LocationVector.generate_location_vector(self, branch[subtree], ("{0}[{1}]".format(index, subtree)))


class HelperFunctions(object):
    @staticmethod
    def is_number(s):
        m = re.findall(r"(^[0-9]*[0-9., ]*$)", s)
        return m

    @staticmethod
    def all_lowercase(s):
        m = re.search("[a-z]", s)
        return m


class WordTagger(HelperFunctions):
    """
        parse xml and generate location vector
    """
    spell_checker_us = enchant.Dict('en_US')
    spell_checker_gb = enchant.Dict('en_GB')
    spell_checker_au = enchant.Dict('en_AU')

    def __init__(self, doc_id, individual_doc, words, doc_bigrams, doc_trigrams, doc_fourgrams,
                 doc_fivegrams, doc_corpus, doc_corpus_bigrams, doc_corpus_trigrams, doc_corpus_fourgrams,
                 doc_corpus_fivegrams, count, word_count_list, bigram_count_list, trigram_count_list,
                 fourgram_count_list, fivegram_count_list):
        super(WordTagger, self).__init__()
        self.word_location = []
        self.doc_id = doc_id
        self.doc = individual_doc

        self.doc_words = words
        self.bi_grams = doc_bigrams
        self.tri_grams = doc_trigrams
        self.four_grams = doc_fourgrams
        self.five_grams = doc_fivegrams

        self.corpus = doc_corpus
        self.corpus_bigrams = doc_corpus_bigrams
        self.corpus_trigrams = doc_corpus_trigrams
        self.corpus_fourgrams = doc_corpus_fourgrams
        self.corpus_fivegrams = doc_corpus_fivegrams

        self.doc_count = count
        self.doc_word_count_list = word_count_list
        self.doc_bi_gram_count_list = bigram_count_list
        self.doc_tri_gram_count_list = trigram_count_list
        self.doc_four_gram_count_list = fourgram_count_list
        self.doc_five_gram_count_list = fivegram_count_list

        self.tf_idf_list = {}
        self.tf_idf_bigram_list = {}
        self.tf_idf_trigram_list = {}
        self.tf_idf_fourgram_list = {}
        self.tf_idf_fivegram_list = {}

        self.doc_word = ''
        self.bi_gram = ''
        self.tri_gram = ''
        self.four_gram = ''
        self.five_gram = ''

        self.word_location_index = ''
        self.signature_map = ''
        self.bi_gram_index = ''
        self.tri_gram_index = ''
        self.four_gram_index = ''
        self.five_gram_index = ''

        self.tf = 0.0
        self.tf_bigram = 0.0
        self.tf_trigram = 0.0
        self.tf_fourgram = 0.0
        self.tf_fivegram = 0.0

        self.idf = 0.0
        self.idf_bigram = 0.0
        self.idf_trigram = 0.0
        self.idf_fourgram = 0.0
        self.idf_fivegram = 0.0

        self.tfidf = 0.0
        self.tfidf_bigram = 0.0
        self.tfidf_trigram = 0.0
        self.tfidf_fourgram = 0.0
        self.tfidf_fivegram = 0.0

        # word bags
        self.common_eng_words = {}
        self.abbreviations = {}

        self.nouns_unigrams = {}
        self.verbs_unigrams = {}
        self.all_caps_unigrams = {}
        self.numbers_unigrams = {}

        self.bigram_nnp_nnp = {}
        self.bigram_nnp_nn = {}
        self.bigram_nn_nn = {}
        self.bigram_nn_nns = {}
        self.bigram_nn_vbd = {}

        self.trigram_nnp_nnp_nnp = {}
        self.trigram_nnp_nnp_nn = {}
        self.trigram_nnp_nn_nn = {}
        self.trigram_nn_nn_nn = {}
        self.trigram_nn_nn_cd = {}
        self.trigram_nn_nns_cd = {}

        self.fourgram_nnp_nnp_nnp_nnp = {}

        self.fivegram_nnp_nnp_nnp_nnp_nnp = {}

    def parse_xml(self):
        #parser = etree.XMLParser(ns_clean=True, remove_pis=True, recover=True)
        parser = etree.XMLParser(recover=True)
        self.doc = '<xml>' + self.doc + '</xml>'
        f = etree.parse(BytesIO(self.doc), parser)
        fstring = etree.tostring(f, pretty_print=True)
        element = etree.fromstring(fstring)
        return element

    def generate_location_vector(self, branch, index):
        """
            generating location vector for every token (word) in doc
        """
        if branch.text is not None:
            branch.text = branch.text.encode('ascii', 'ignore')

            if not branch.getchildren():
                statements = branch.text.split('. ')

                for statement in range(0, len(statements)):
                    statement_location = (("{0}[{1}]".format(index, statement)), statements[statement])
                    words = statements[statement].split()
                    statement_loc_vec = statement_location[0]
                    for doc_word in range(0, len(words)):
                        word_location = (("{0}[{1}][{2}]".format(index, statement, doc_word)), words[doc_word])
                        symbols = ".,[]();:<>+=&+%!@#~?{}|"
                        whitespace = "                       "
                        replace = maketrans(symbols, whitespace)
                        doc_word = word_location[1].translate(replace)
                        doc_word = doc_word.lstrip()
                        doc_word = doc_word.rstrip()

                        if len(doc_word) > 1 and not len(doc_word) > 16:
                            self.doc_word = doc_word
                            word_location_index = word_location[0].replace('][', ' ')
                            word_location_index = word_location_index.replace('[', '')
                            self.word_location_index = word_location_index.replace(']', '')
                            WordTagger.word_matcher(self)

                    doc_bigrams = bigrams(words)
                    if not len(doc_bigrams) < 1:
                        for i, bi_gram in enumerate(doc_bigrams):
                            self.bi_gram = ' '.join(bi_gram)
                            statement_loc_vec = statement_loc_vec.replace('][', ' ')
                            statement_loc_vec = statement_loc_vec.replace('[', '')
                            statement_loc_vec = statement_loc_vec.replace(']', '')
                            self.bi_gram_index = statement_loc_vec + ' ' + str(
                                i) + ' | ' + statement_loc_vec + ' ' + str(i + 1)
                            WordTagger.word_matcher_bigram(self, self.bi_gram)

                    doc_trigrams = trigrams(words)
                    if not len(doc_trigrams) < 1:
                        for i, tri_gram in enumerate(doc_trigrams):
                            self.tri_gram = ' '.join(tri_gram)
                            statement_loc_vec = statement_loc_vec.replace('][', ' ')
                            statement_loc_vec = statement_loc_vec.replace('[', '')
                            statement_loc_vec = statement_loc_vec.replace(']', '')
                            self.tri_gram_index = statement_loc_vec + ' ' + str(
                                i) + ' | ' + statement_loc_vec + ' ' + str(
                                i + 1) + ' | ' + statement_loc_vec + ' ' + str(i + 2)
                            WordTagger.word_matcher_trigram(self, self.tri_gram)

                    doc_fourgrams = ngrams(words, 4)
                    if not len(doc_fourgrams) < 1:
                        for i, four_gram in enumerate(doc_fourgrams):
                            self.four_gram = ' '.join(four_gram)
                            statement_loc_vec = statement_loc_vec.replace('][', ' ')
                            statement_loc_vec = statement_loc_vec.replace('[', '')
                            statement_loc_vec = statement_loc_vec.replace(']', '')
                            self.four_gram_index = statement_loc_vec + ' ' + str(
                                i) + ' | ' + statement_loc_vec + ' ' + str(
                                i + 1) + ' | ' + statement_loc_vec + ' ' + str(
                                i + 2) + ' | ' + statement_loc_vec + ' ' + str(i + 3)
                            WordTagger.word_matcher_fourgram(self, self.four_gram)

                    doc_fivegrams = ngrams(words, 5)
                    if not len(doc_fivegrams) < 1:
                        for five_gram in doc_fivegrams:
                            self.five_gram = ' '.join(five_gram)
                            statement_loc_vec = statement_loc_vec.replace('][', ' ')
                            statement_loc_vec = statement_loc_vec.replace('[', '')
                            statement_loc_vec = statement_loc_vec.replace(']', '')
                            self.five_gram_index = statement_loc_vec + ' ' + str(
                                i) + ' | ' + statement_loc_vec + ' ' + str(
                                i + 1) + ' | ' + statement_loc_vec + ' ' + str(
                                i + 2) + ' | ' + statement_loc_vec + ' ' + str(
                                i + 3) + ' | ' + statement_loc_vec + ' ' + str(i + 4)
                            WordTagger.word_matcher_fivegram(self, self.five_gram)

            else:
                for subtree in range(0, len(branch)):
                    WordTagger.generate_location_vector(self, branch[subtree], ("{0}[{1}]".format(index, subtree)))

    def word_matcher(self):
        WordTagger.tf(self)
        WordTagger.idf(self)
        WordTagger.tf_idf(self)
        WordTagger.english_dict_match(self)
        WordTagger.number_match(self)
        WordTagger.repetitive_words(self)
        WordTagger.pos_tagging_unigrams(self)

    def word_matcher_bigram(self, bi_gram):
        WordTagger.tf_bigram(self)
        WordTagger.idf_bigram(self)
        WordTagger.tf_idf_bigram(self)
        WordTagger.first_letter_upper(bi_gram)
        WordTagger.pos_tagging(self, bi_gram)

    def word_matcher_trigram(self, tri_gram):
        WordTagger.tf_trigram(self)
        WordTagger.idf_trigram(self)
        WordTagger.tf_idf_trigram(self)
        WordTagger.first_letter_upper(tri_gram)
        WordTagger.pos_tagging(self, tri_gram)

    def word_matcher_fourgram(self, four_gram):
        WordTagger.tf_fourgram(self)
        WordTagger.idf_fourgram(self)
        WordTagger.tf_idf_fourgram(self)
        WordTagger.first_letter_upper(four_gram)
        WordTagger.pos_tagging(self, four_gram)

    def word_matcher_fivegram(self, five_gram):
        WordTagger.tf_fivegram(self)
        WordTagger.idf_fivegram(self)
        WordTagger.tf_idf_fivegram(self)
        WordTagger.first_letter_upper(five_gram)
        WordTagger.pos_tagging(self, five_gram)

    def tf(self):
        word_count = self.doc_words.count(self.doc_word)
        self.tf = word_count / float(len(self.doc_words))

    def tf_bigram(self):
        bigram_count = self.bi_grams.count(self.bi_gram)
        self.tf_bigram = bigram_count / float(len(self.bi_grams))

    def tf_trigram(self):
        trigram_count = self.tri_grams.count(self.tri_gram)
        self.tf_trigram = trigram_count / float(len(self.tri_grams))

    def tf_fourgram(self):
        fourgram_count = self.four_grams.count(self.four_gram)
        self.tf_fourgram = fourgram_count / float(len(self.four_grams))

    def tf_fivegram(self):
        fivegram_count = self.five_grams.count(self.five_gram)
        self.tf_fivegram = fivegram_count / float(len(self.five_grams))

    def idf(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.doc_word_count_list)):
            end += self.doc_word_count_list[i]
            if self.doc_word in self.corpus[start:end]:
                word_occurrence += 1
            start = end + 1
        self.idf = log10(float(self.doc_count + 1) / (word_occurrence + 1))

    def idf_bigram(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.doc_bi_gram_count_list)):
            end += self.doc_bi_gram_count_list[i]
            if self.bi_gram in self.corpus_bigrams[start:end]:
                word_occurrence += 1
            start = end + 1
        self.idf_bigram = log10(float(self.doc_count + 1) / (word_occurrence + 1))

    def idf_trigram(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.doc_tri_gram_count_list)):
            end += self.doc_tri_gram_count_list[i]
            if self.tri_gram in self.corpus_trigrams[start:end]:
                word_occurrence += 1
            start = end + 1
        self.idf_trigram = log10(float(self.doc_count + 1) / (word_occurrence + 1))

    def idf_fourgram(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.doc_four_gram_count_list)):
            end += self.doc_four_gram_count_list[i]
            if self.four_gram in self.corpus_fourgrams[start:end]:
                word_occurrence += 1
            start = end + 1
        self.idf_fourgram = log10(float(self.doc_count + 1) / (word_occurrence + 1))

    def idf_fivegram(self):
        word_occurrence = 0
        start, end = 0, 0
        for i in range(0, len(self.doc_five_gram_count_list)):
            end += self.doc_five_gram_count_list[i]
            if self.five_gram in self.corpus_fivegrams[start:end]:
                word_occurrence += 1
            start = end + 1
        self.idf_fivegram = log10(float(self.doc_count + 1) / (word_occurrence + 1))

    def tf_idf(self):
        self.tfidf = self.tf * self.idf
        self.tf_idf_list[self.tfidf, self.word_location_index] = self.doc_word

    def tf_idf_bigram(self):
        self.tfidf_bigram = self.tf_bigram * self.idf_bigram
        self.tf_idf_bigram_list[self.tfidf_bigram, self.bi_gram_index] = self.bi_gram

    def tf_idf_trigram(self):
        self.tfidf_trigram = self.tf_trigram * self.idf_trigram
        self.tf_idf_trigram_list[self.tfidf_trigram, self.tri_gram_index] = self.tri_gram

    def tf_idf_fourgram(self):
        self.tfidf_fourgram = self.tf_fourgram * self.idf_fourgram
        self.tf_idf_fourgram_list[self.tfidf_fourgram, self.four_gram_index] = self.four_gram

    def tf_idf_fivegram(self):
        self.tfidf_fivegram = self.tf_fivegram * self.idf_fivegram
        self.tf_idf_fivegram_list[self.tfidf_fivegram, self.five_gram_index] = self.five_gram

    def english_dict_match(self):
        """
            matching doc word to English dictionaries
        """
        spell_checker_us = enchant.Dict('en_US')
        spell_checker_gb = enchant.Dict('en_GB')
        spell_checker_au = enchant.Dict('en_AU')

        if spell_checker_us.check(self.doc_word.lower()) is True or spell_checker_gb.check(
                self.doc_word.lower()) is True or spell_checker_au.check(self.doc_word.lower()) is True:
            if not self.doc_word.lower() in (corpus.stopwords.words('english')):
                self.common_eng_words[self.doc_word] = self.tfidf

        if HelperFunctions.all_lowercase(self.doc_word) is None and spell_checker_us.check(
                self.doc_word) is False:
            pass

    def number_match(self):
        if HelperFunctions.is_number(self.doc_word):
            pass

    def repetitive_words(self):
        if self.idf == 0.0:
            pass

    def pos_tagging_unigrams(self):
        pos = pos_tag([self.doc_word])
        # NN or NNP --> Nouns
        # filter all unigrams whose tf_idf score = 1
        if self.tfidf != 0.0:
            #if not self.doc_word.lower() in (corpus.stopwords.words('english')) and not self.idf == 1.0 and \
                    #(pos[0][1] == 'NN' or pos[0][1] == 'NNP' or pos[0][1] == 'NNS'):
            if not self.doc_word.lower() in (corpus.stopwords.words('english')) and not self.idf == 1.0 and \
                (pos[0][1] == 'NNP'):
                self.nouns_unigrams[self.doc_word] = self.tfidf

            if not self.doc_word.lower() in (corpus.stopwords.words('english')) and not self.idf == 1.0 and \
                            pos[0][1] == 'VB' or pos[0][1] == 'VBD':
                self.verbs_unigrams[self.doc_word] = self.tfidf
            if not self.doc_word.lower() in (corpus.stopwords.words('english')) and not self.idf == 1.0:
                if re.search(r'\b[A-Z]+(?:\W*[A-Z]+)*\b', self.doc_word):
                    self.all_caps_unigrams[self.doc_word] = self.tfidf
                if re.search(r'^[0-9]', self.doc_word):
                    self.numbers_unigrams[self.doc_word] = self.tfidf

    @staticmethod
    def first_letter_upper(string):
        cap_count = 0
        words = string.split()
        for doc_word in words:
            if doc_word[0].isupper():
                cap_count += 1
        if cap_count == len(words):
            pass

    def pos_tagging(self, string):
        """

        POS Tagger for bigrams | trigrams | 4-grams | 5-grams
        """
        words = word_tokenize(string)
        pos = pos_tag(words)
        pos = [x[1] for x in pos]

        # POS word bags for bigrams
        if len(pos) == 2 and pos[0] == 'NNP' and pos[1] == 'NNP':
            self.bigram_nnp_nnp[string] = self.tfidf_bigram

        if len(pos) == 2 and pos[0] == 'NNP' and pos[1] == 'NN':
            self.bigram_nnp_nn[string] = self.tfidf_bigram

        if len(pos) == 2 and pos[0] == 'NN' and pos[1] == 'NN':
            self.bigram_nn_nn[string] = self.tfidf_bigram

        if len(pos) == 2 and pos[0] == 'NN' and pos[1] == 'NNS':
            self.bigram_nn_nns[string] = self.tfidf_bigram

        # POS word bags for trigrams
        if len(pos) == 3 and pos[0] == 'NNP' and pos[1] == 'NNP' and pos[2] == 'NNP':
            self.trigram_nnp_nnp_nnp[string] = self.tfidf_trigram

        if len(pos) == 3 and pos[0] == 'NNP' and pos[1] == 'NNP' and pos[2] == 'NN':
            self.trigram_nnp_nnp_nn[string] = self.tfidf_trigram

        if len(pos) == 3 and pos[0] == 'NNP' and pos[1] == 'NN' and pos[2] == 'NN':
            self.trigram_nnp_nn_nn[string] = self.tfidf_trigram

        if len(pos) == 3 and pos[0] == 'NN' and pos[1] == 'NN' and pos[2] == 'NN':
            self.trigram_nn_nn_nn[string] = self.tfidf_trigram

        if len(pos) == 3 and pos[0] == 'NN' and pos[1] == 'NN' and pos[2] == 'CD':
            self.trigram_nn_nn_cd[string] = self.tfidf_trigram

        if len(pos) == 3 and pos[0] == 'NN' and pos[1] == 'NNS' and pos[2] == 'CD':
            self.trigram_nn_nns_cd[string] = self.tfidf_trigram

        # POS word bags for 4-grams
        if len(pos) == 4 and pos[0] == 'NNP' and pos[1] == 'NNP' and pos[2] == 'NNP' and pos[
            3] == 'NNP':
            self.fourgram_nnp_nnp_nnp_nnp[string] = self.tfidf_fourgram

        # POS word bags for 5-grams
        if len(pos) == 5 and pos[0] == 'NNP' and pos[1] == 'NNP' and pos[2] == 'NNP' and pos[
            3] == 'NNP' and pos[4] == 'NNP':
            self.fivegram_nnp_nnp_nnp_nnp_nnp[string] = self.tfidf_fivegram