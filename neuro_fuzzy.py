from __future__ import division

__author__ = 'Arunprasath Shankar'
__copyright__ = 'Copyright 2012, Arunprasath Shankar'
__license__ = 'GPL'
__version__ = '1.0.1'
__email__ = 'axs918@case.edu'
import itertools
from operator import itemgetter


class NeuroFuzzySystem(object):
    def __init__(self):
        self.word_list = []
        self.cog_list = []
        self.word_info = {}

        self.bigram_list = []
        self.cog_list_bigrams = []
        self.bigram_info = {}

        self.trigram_list = []
        self.cog_list_trigrams = []
        self.trigram_info = {}

        self.fourgram_list = []
        self.cog_list_fourgrams = []
        self.fourgram_info = {}

        self.fivegram_list = []
        self.cog_list_fivegrams = []
        self.fivegram_info = {}

        self.pi_bundle_unigrams = {}
        self.pi_bundle_bigrams = {}
        self.pi_bundle_trigrams = {}
        self.pi_bundle_fourgrams = {}
        self.pi_bundle_fivegrams = {}
        self.mfs = []

    def neuro_fuzzy_modelling(self, tf_idf_list, u1, u2, u3, u4, u5, tf_idf_bigram_list, b1, b2, b3, b4,
                              tf_idf_trigram_list, t1, t2, t3, t4, t5, t6, tf_idf_fourgram_list, f1,
                              tf_idf_fivegram_list, p1):
        """
        @param tf_idf_list: list of unigrams with info like tf_idf and location index
        @param tf_idf_bigram_list:
        @param tf_idf_trigram_list:
        @param tf_idf_fourgram_list:
        @param tf_idf_fivegram_list:
        """
        bag_names = {'u1': 'common English word',
                     'u2': 'unigram noun',
                     'u3': 'unigram all upper',
                     'u4': 'unigram number'}
        u1 = {item[0]: item[1:] for item in u1}
        u2 = {item[0]: item[1:] for item in u2}
        u3 = {item[0]: item[1:] for item in u3}
        u4 = {item[0]: item[1:] for item in u4}
        u5 = {item[0]: item[1:] for item in u5}
        b1 = {item[0]: item[1:] for item in b1}
        b2 = {item[0]: item[1:] for item in b2}
        b3 = {item[0]: item[1:] for item in b3}
        b4 = {item[0]: item[1:] for item in b4}
        t1 = {item[0]: item[1:] for item in t1}
        t2 = {item[0]: item[1:] for item in t2}
        t3 = {item[0]: item[1:] for item in t3}
        t4 = {item[0]: item[1:] for item in t4}
        t5 = {item[0]: item[1:] for item in t5}
        t6 = {item[0]: item[1:] for item in t6}
        f1 = {item[0]: item[1:] for item in f1}
        p1 = {item[0]: item[1:] for item in p1}
        for info, word in tf_idf_list.iteritems():
        # filter all unigrams whose tf_idf score = 1
            if info[0] != 0.0:
                try:
                    activated_fuzzy_sets = []
                    u1_nrn_info = u1.get(word, None)
                    if u1_nrn_info is not None:
                        activated_fuzzy_sets.append(bag_names.get('u1'))
                    u2_nrn_info = u2.get(word, None)
                    if u2_nrn_info is not None:
                        activated_fuzzy_sets.append(bag_names.get('u2'))
                    u3_nrn_info = u3.get(word, None)
                    if u3_nrn_info is not None:
                        activated_fuzzy_sets.append(bag_names.get('u3'))
                    u4_nrn_info = u4.get(word, None)
                    if u4_nrn_info is not None:
                        activated_fuzzy_sets.append(bag_names.get('u4'))
                    u5_nrn_info = u5.get(word, None)
                    if u5_nrn_info is not None:
                        activated_fuzzy_sets.append(bag_names.get('u5'))
                except KeyError:
                    continue

                self.mfs = []
                self.wts = []
                if u1_nrn_info is not None:
                    u1_mf1 = u1_nrn_info[1] * u1_nrn_info[2] - 2
                    u1_mf2 = u1_nrn_info[3] * u1_nrn_info[4] - 2
                    self.mfs.append([u1_mf1, u1_mf2])
                    self.wts.append(u1_nrn_info[2])
                    self.wts.append(u1_nrn_info[4])
                if u2_nrn_info is not None:
                    u2_mf1 = u2_nrn_info[1] * u2_nrn_info[2] + 3
                    u2_mf2 = u2_nrn_info[3] * u2_nrn_info[4] + 3
                    self.mfs.append([u2_mf1, u2_mf2])
                    self.wts.append(u2_nrn_info[2])
                    self.wts.append(u2_nrn_info[4])
                if u3_nrn_info is not None:
                    u3_mf1 = u3_nrn_info[1] * u3_nrn_info[2]
                    u3_mf2 = u3_nrn_info[3] * u3_nrn_info[4]
                    self.mfs.append([u3_mf1, u3_mf2])
                    self.wts.append(u3_nrn_info[2])
                    self.wts.append(u3_nrn_info[4])
                if u4_nrn_info is not None:
                    u4_mf1 = u4_nrn_info[1] * u4_nrn_info[2]
                    u4_mf2 = u4_nrn_info[3] * u4_nrn_info[4]
                    self.mfs.append([u4_mf1, u4_mf2])
                    self.wts.append(u4_nrn_info[2])
                    self.wts.append(u4_nrn_info[4])
                if u5_nrn_info is not None:
                    u5_mf1 = u5_nrn_info[1] * u5_nrn_info[2]  # verbs are potential predicates
                    u5_mf2 = u5_nrn_info[3] * u5_nrn_info[4]
                    self.mfs.append([u5_mf1, u5_mf2])
                    self.wts.append(u5_nrn_info[2])
                    self.wts.append(u5_nrn_info[4])
                    
                if len(self.mfs) > 0:
                    weights = sum(self.wts)
                    rule_inputs = list(itertools.product(*self.mfs))
                    number_of_wordbags = len(self.mfs)
                    number_of_rules = len(rule_inputs)
                    number_of_weights = len(self.wts)
                    weight_factor = number_of_wordbags * number_of_rules / number_of_weights
                    weights *= weight_factor
                    rule_inputs = sum([sum(r) for r in rule_inputs])
                    self.defuzzify_unigrams(word, rule_inputs, weights, info)

        for info, bigram in tf_idf_bigram_list.iteritems():
            if info[0] != 0.0:
                try:
                    b1_nrn_info = b1.get(bigram, None)
                    b2_nrn_info = b2.get(bigram, None)
                    b3_nrn_info = b3.get(bigram, None)
                    b4_nrn_info = b4.get(bigram, None)
                except KeyError:
                    continue

                self.mfs = []
                self.wts = []
                if b1_nrn_info is not None:
                    b1_mf1 = b1_nrn_info[1] * b1_nrn_info[2]
                    b1_mf2 = b1_nrn_info[3] * b1_nrn_info[4]
                    self.mfs.append([b1_mf1, b1_mf2])
                    self.wts.append(b1_nrn_info[2])
                    self.wts.append(b1_nrn_info[4])
                if b2_nrn_info is not None:
                    b2_mf1 = b2_nrn_info[1] * b2_nrn_info[2]
                    b2_mf2 = b2_nrn_info[3] * b2_nrn_info[4]
                    self.mfs.append([b2_mf1, b2_mf2])
                    self.wts.append(b2_nrn_info[2])
                    self.wts.append(b2_nrn_info[4])
                if b3_nrn_info is not None:
                    b3_mf1 = b3_nrn_info[1] * b3_nrn_info[2]
                    b3_mf2 = b3_nrn_info[3] * b3_nrn_info[4]
                    self.mfs.append([b3_mf1, b3_mf2])
                    self.wts.append(b3_nrn_info[2])
                    self.wts.append(b3_nrn_info[4])
                if b4_nrn_info is not None:
                    b4_mf1 = b4_nrn_info[1] * b4_nrn_info[2]
                    b4_mf2 = b4_nrn_info[3] * b4_nrn_info[4]
                    self.mfs.append([b4_mf1, b4_mf2])
                    self.wts.append(b4_nrn_info[2])
                    self.wts.append(b4_nrn_info[4])
                if len(self.mfs) > 0:
                    weights = sum(self.wts)
                    rule_inputs = list(itertools.product(*self.mfs))
                    number_of_wordbags = len(self.mfs)
                    number_of_rules = len(rule_inputs)
                    number_of_weights = len(self.wts)
                    weight_factor = number_of_wordbags * number_of_rules / number_of_weights
                    weights *= weight_factor
                    rule_inputs = sum([sum(r) for r in rule_inputs])
                    self.defuzzify_bigrams(bigram, rule_inputs, weights, info)

        for info, trigram in tf_idf_trigram_list.iteritems():
            if info[0] != 0.0:
                try:
                    t1_nrn_info = t1.get(trigram, None)
                    t2_nrn_info = t2.get(trigram, None)
                    t3_nrn_info = t3.get(trigram, None)
                    t4_nrn_info = t4.get(trigram, None)
                    t5_nrn_info = t5.get(trigram, None)
                    t6_nrn_info = t6.get(trigram, None)
                except KeyError:
                    continue

                self.mfs = []
                self.wts = []
                if t1_nrn_info is not None:
                    t1_mf1 = t1_nrn_info[1] * t1_nrn_info[2]
                    t1_mf2 = t1_nrn_info[3] * t1_nrn_info[4]
                    self.mfs.append([t1_mf1, t1_mf2])
                    self.wts.append(t1_nrn_info[2])
                    self.wts.append(t1_nrn_info[4])
                if t2_nrn_info is not None:
                    t2_mf1 = t2_nrn_info[1] * t2_nrn_info[2]
                    t2_mf2 = t2_nrn_info[3] * t2_nrn_info[4]
                    self.mfs.append([t2_mf1, t2_mf2])
                    self.wts.append(t2_nrn_info[2])
                    self.wts.append(t2_nrn_info[4])
                if t3_nrn_info is not None:
                    t3_mf1 = t3_nrn_info[1] * t3_nrn_info[2]
                    t3_mf2 = t3_nrn_info[3] * t3_nrn_info[4]
                    self.mfs.append([t3_mf1, t3_mf2])
                    self.wts.append(t3_nrn_info[2])
                    self.wts.append(t3_nrn_info[4])
                if t4_nrn_info is not None:
                    t4_mf1 = t4_nrn_info[1] * t4_nrn_info[2]
                    t4_mf2 = t4_nrn_info[3] * t4_nrn_info[4]
                    self.mfs.append([t4_mf1, t4_mf2])
                    self.wts.append(t4_nrn_info[2])
                    self.wts.append(t4_nrn_info[4])
                if t5_nrn_info is not None:
                    t5_mf1 = t5_nrn_info[1] * t5_nrn_info[2]
                    t5_mf2 = t5_nrn_info[3] * t5_nrn_info[4]
                    self.mfs.append([t5_mf1, t5_mf2])
                    self.wts.append(t5_nrn_info[2])
                    self.wts.append(t5_nrn_info[4])
                if t6_nrn_info is not None:
                    t6_mf1 = t6_nrn_info[1] * t6_nrn_info[2]
                    t6_mf2 = t6_nrn_info[3] * t6_nrn_info[4]
                    self.mfs.append([t6_mf1, t6_mf2])
                    self.wts.append(t6_nrn_info[2])
                    self.wts.append(t6_nrn_info[4])
                if len(self.mfs) > 0:
                    weights = sum(self.wts)
                    rule_inputs = list(itertools.product(*self.mfs))
                    number_of_wordbags = len(self.mfs)
                    number_of_rules = len(rule_inputs)
                    number_of_weights = len(self.wts)
                    weight_factor = number_of_wordbags * number_of_rules / number_of_weights
                    weights *= weight_factor
                    rule_inputs = sum([sum(r) for r in rule_inputs])
                    self.defuzzify_trigrams(trigram, rule_inputs, weights, info)

        for info, fourgram in tf_idf_fourgram_list.iteritems():
            if info[0] != 0.0:
                try:
                    f1_nrn_info = f1.get(fourgram, None)
                except KeyError:
                    continue

                self.mfs = []
                self.wts = []
                if f1_nrn_info is not None:
                    f1_mf1 = f1_nrn_info[1] * f1_nrn_info[2]
                    f1_mf2 = f1_nrn_info[3] * f1_nrn_info[4]
                    self.mfs.append([f1_mf1, f1_mf2])
                    self.wts.append(f1_nrn_info[2])
                    self.wts.append(f1_nrn_info[4])
                if len(self.mfs) > 0:
                    weights = sum(self.wts)
                    rule_inputs = list(itertools.product(*self.mfs))
                    number_of_wordbags = len(self.mfs)
                    number_of_rules = len(rule_inputs)
                    number_of_weights = len(self.wts)
                    weight_factor = number_of_wordbags * number_of_rules / number_of_weights
                    weights *= weight_factor
                    rule_inputs = sum([sum(r) for r in rule_inputs])
                    self.defuzzify_fourgrams(fourgram, rule_inputs, weights, info)

        for info, fivegram in tf_idf_fivegram_list.iteritems():
            if info[0] != 0.0:
                try:
                    p1_nrn_info = p1.get(fivegram, None)
                except KeyError:
                    continue

                self.mfs = []
                self.wts = []
                if p1_nrn_info is not None:
                    p1_mf1 = p1_nrn_info[1] * p1_nrn_info[2]
                    p1_mf2 = p1_nrn_info[3] * p1_nrn_info[4]
                    self.mfs.append([p1_mf1, p1_mf2])
                    self.wts.append(p1_nrn_info[2])
                    self.wts.append(p1_nrn_info[4])
                if len(self.mfs) > 0:
                    weights = sum(self.wts)
                    rule_inputs = list(itertools.product(*self.mfs))
                    number_of_wordbags = len(self.mfs)
                    number_of_rules = len(rule_inputs)
                    number_of_weights = len(self.wts)
                    weight_factor = number_of_wordbags * number_of_rules / number_of_weights
                    weights *= weight_factor
                    rule_inputs = sum([sum(r) for r in rule_inputs])
                    self.defuzzify_fivegrams(fivegram, rule_inputs, weights, info)

    def defuzzify_unigrams(self, word, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.word_list.append(word)
        self.cog_list.append(cog)
        self.word_info[info] = word

    def defuzzify_bigrams(self, bigram, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.bigram_list.append(bigram)
        self.cog_list_bigrams.append(cog)
        self.bigram_info[info] = bigram

    def defuzzify_trigrams(self, trigram, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.trigram_list.append(trigram)
        self.cog_list_trigrams.append(cog)
        self.trigram_info[info] = trigram

    def defuzzify_fourgrams(self, fourgram, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.fourgram_list.append(fourgram)
        self.cog_list_fourgrams.append(cog)
        self.fourgram_info[info] = fourgram

    def defuzzify_fivegrams(self, fivegram, rule_inputs, weights, info):
        cog = rule_inputs / weights
        self.fivegram_list.append(fivegram)
        self.cog_list_fivegrams.append(cog)
        self.fivegram_info[info] = fivegram

    def norm_cog_unigrams(self):
        for k, v in self.word_info.iteritems():
            print k, v

        if not len(self.cog_list) < 1:
            max_cog = max(self.cog_list)
            self.cog_list = [cog / max_cog for cog in self.cog_list]
            word_rank = dict(zip(self.word_list, self.cog_list))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** UNIGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                uni_gram_lv_list = [item[1]]
                for info, word in self.word_info.iteritems():
                    if item[0] == word:
                        print info
                        uni_gram_lv_list.append(info)

                self.pi_bundle_unigrams[item[0]] = uni_gram_lv_list

        else:
            print '*********** UNIGRAMS ***********'
            print None

    def norm_cog_bigrams(self):
        if not len(self.cog_list_bigrams) < 1:
            print self.cog_list_bigrams
            max_cog = max(self.cog_list_bigrams)
            self.cog_list_bigrams = [cog / max_cog for cog in self.cog_list_bigrams]
            word_rank = dict(zip(self.bigram_list, self.cog_list_bigrams))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** BIGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                bi_gram_lv_list = [item[1]]
                for info, bigram in self.bigram_info.iteritems():
                    if item[0] == bigram:
                        print info
                        bi_gram_lv_list.append(info)

                self.pi_bundle_bigrams[item[0]] = bi_gram_lv_list

        else:
            print '*********** BIGRAMS ***********'
            print None

    def norm_cog_trigrams(self):
        if not len(self.cog_list_trigrams) < 1:
            max_cog = max(self.cog_list_trigrams)
            self.cog_list_trigrams = [cog / max_cog for cog in self.cog_list_trigrams]
            word_rank = dict(zip(self.trigram_list, self.cog_list_trigrams))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** TRIGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                tri_gram_lv_list = [item[1]]
                for info, trigram in self.trigram_info.iteritems():
                    if item[0] == trigram:
                        print info
                        tri_gram_lv_list.append(info)

                self.pi_bundle_trigrams[item[0]] = tri_gram_lv_list

        else:
            print '*********** TRIGRAMS ***********'
            print None

    def norm_cog_fourgrams(self):
        if not len(self.cog_list_fourgrams) < 1:
            max_cog = max(self.cog_list_fourgrams)
            self.cog_list_fourgrams = [cog / max_cog for cog in self.cog_list_fourgrams]
            word_rank = dict(zip(self.fourgram_list, self.cog_list_fourgrams))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** FOURGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                four_gram_lv_list = [item[1]]
                for info, fourgram in self.fourgram_info.iteritems():
                    if item[0] == fourgram:
                        print info
                        four_gram_lv_list.append(info)

                self.pi_bundle_fourgrams[item[0]] = four_gram_lv_list

        else:
            print '*********** FOURGRAMS ***********'
            print None

    def norm_cog_fivegrams(self):
        if not len(self.cog_list_fivegrams) < 1:
            max_cog = max(self.cog_list_fivegrams)
            self.cog_list_fivegrams = [cog / max_cog for cog in self.cog_list_fivegrams]
            word_rank = dict(zip(self.fivegram_list, self.cog_list_fivegrams))
            sorted_word_rank = sorted(word_rank.iteritems(), key=itemgetter(1))
            print '*********** FIVEGRAMS ***********'
            for item in sorted_word_rank:
                print item[0], item[1]
                five_gram_lv_list = [item[1]]
                for info, fivegram in self.fivegram_info.iteritems():
                    if item[0] == fivegram:
                        print info
                        five_gram_lv_list.append(info)

                self.pi_bundle_fivegrams[item[0]] = five_gram_lv_list

        else:
            print '*********** FIVEGRAMS ***********'
            print None