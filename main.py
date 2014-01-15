# -*- coding: utf-8 -*-
import sys
import os
import fnmatch
from master_dag import MasterDAG
from master_uag import MasterUAG

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from doc_analyzer import LocationVector, WordTagger
from range_estimator import RangeCalculator
#from fuzzy_plot import FuzzyPlotFilterI
#from scatter_plot import ScatterPlot
from concept_skeleton import ConceptSkeleton
from proximity_finder import ProximityFinder
from neuro_fuzzy import NeuroFuzzySystem
from fuzzy_concepts import FuzzyConcept
from dom import DegreeOfMembership
from corpus import Corpus
import pygraphviz as pgv
import csv

if __name__ == '__main__':
    doc_count = 0
    doc_word_count_list, corpus_words = [], []
    doc_bi_gram_count_list, corpus_bi_grams = [], []
    doc_tri_gram_count_list, corpus_tri_grams = [], []
    doc_four_gram_count_list, corpus_four_grams = [], []
    doc_five_gram_count_list, corpus_five_grams = [], []

    def recurse_dir(path, file_type):
        for root, dirs, docs in os.walk(path):
            for document in fnmatch.filter(docs, file_type):
                yield os.path.join(root, document)

    # building corpus of docs
    corpus = []
    corpus_bigrams = []
    corpus_trigrams = []
    corpus_fourgrams = []
    corpus_fivegrams = []
    for doc in recurse_dir(r'./epics', '*.txt'):
        doc_file = open(doc, 'rb')
        doc = doc_file.read()
        doc_words = []
        bi_grams = []
        tri_grams = []
        four_grams = []
        five_grams = []

        cor = Corpus(doc, doc_words, bi_grams, tri_grams, four_grams, five_grams)
        cor.generate_location_vector(cor.parse_xml(), [0])
        doc_count += 1

        doc_word_count = len(doc_words)
        doc_word_count_list.append(doc_word_count)
        corpus_words.append(doc_words)

        doc_bi_gram_count = len(bi_grams)
        doc_bi_gram_count_list.append(doc_bi_gram_count)
        corpus_bi_grams.append(bi_grams)

        doc_tri_gram_count = len(tri_grams)
        doc_tri_gram_count_list.append(doc_tri_gram_count)
        corpus_tri_grams.append(tri_grams)

        doc_four_gram_count = len(four_grams)
        doc_four_gram_count_list.append(doc_four_gram_count)
        corpus_four_grams.append(four_grams)

        doc_five_gram_count = len(five_grams)
        doc_five_gram_count_list.append(doc_five_gram_count)
        corpus_five_grams.append(five_grams)

        for doc_words in corpus_words:
            for word in doc_words:
                corpus.append(word)

        for doc_bi_grams in corpus_bi_grams:
            for bigram in doc_bi_grams:
                corpus_bigrams.append(bigram)

        for doc_tri_grams in corpus_tri_grams:
            for trigram in doc_tri_grams:
                corpus_trigrams.append(trigram)

        for doc_four_grams in corpus_four_grams:
            for fourgram in doc_four_grams:
                corpus_fourgrams.append(fourgram)

        for doc_five_grams in corpus_five_grams:
            for fivegram in doc_five_grams:
                corpus_fivegrams.append(fivegram)

        doc_file.close()

    # ********************************************************************************************************

    # document analysing and creating word bags
    print 'document analysing and creating word bags ...'
    doc_ID = 0
    out_1 = open('PI.csv', 'wb')
    csv_out_1 = csv.writer(out_1)
    out_2 = open('PS.csv', 'wb')
    csv_out_2 = csv.writer(out_2)
    for i, doc in enumerate(recurse_dir(r'./epics', '*.txt')):

        print i, doc
        doc_file = open(doc, 'rb')
        doc = doc_file.read()
        doc_words = []
        bi_grams = []
        tri_grams = []
        four_grams = []
        five_grams = []

        loc_vec = LocationVector(doc, doc_words, bi_grams, tri_grams, four_grams, five_grams)
        loc_vec.generate_location_vector(loc_vec.parse_xml(), [0])

        doc_words = loc_vec.doc_words
        bi_grams = loc_vec.bi_grams
        tri_grams = loc_vec.tri_grams
        four_grams = loc_vec.four_grams
        five_grams = loc_vec.five_grams
        print 'start word tagging ...'

        doc_ID += 1
        tagger = WordTagger(doc_ID, doc, doc_words, bi_grams,
                            tri_grams, four_grams, five_grams, corpus, corpus_bigrams,
                            corpus_trigrams, corpus_fourgrams, corpus_fivegrams, doc_count, doc_word_count_list,
                            doc_bi_gram_count_list, doc_tri_gram_count_list, doc_four_gram_count_list,
                            doc_five_gram_count_list)
        tagger.generate_location_vector(tagger.parse_xml(), [0])

        # ------------- Word Bags ------------
        # tfidf info list of N-grams
        tf_idf_list = tagger.tf_idf_list  # all doc words (unique)
        tf_idf_bigram_list = tagger.tf_idf_bigram_list
        tf_idf_trigram_list = tagger.tf_idf_trigram_list
        tf_idf_fourgram_list = tagger.tf_idf_fourgram_list
        tf_idf_fivegram_list = tagger.tf_idf_fivegram_list

        # word bags Unigrams
        tf_idf_common_eng_words = tagger.common_eng_words  # common english excluding stopwords
        tf_idf_nouns_unigrams = tagger.nouns_unigrams  # uni-gram nouns excluding stopwords
        tf_idf_all_cap_unigrams = tagger.all_caps_unigrams
        tf_idf_numbers_unigrams = tagger.numbers_unigrams

        # ------------ word bags Bigrams -----------

        tf_idf_bigram_NNP_NNP = tagger.bigram_nnp_nnp  # bi-grams with NNP + NNP POS
        tf_idf_bigram_NNP_NN = tagger.bigram_nnp_nn  # bi-grams with NNP + NN POS
        tf_idf_bigram_NN_NN = tagger.bigram_nn_nn  # bi-grams with NN + NN POS
        tf_idf_bigram_NN_NNS = tagger.bigram_nn_nns  # bi-grams with NN + NNS POS eg. clock cycles
        tf_idf_bigram_NN_VBD = tagger.bigram_nn_vbd  # bi-grams with NN + VBD POS eg. wishbone interconnect

        # ------------ word bags Trigrams -----------

        tf_idf_trigram_NNP_NNP_NNP = tagger.trigram_nnp_nnp_nnp  # tri-grams with NNP + NNP + NNP POS
        tf_idf_trigram_NNP_NNP_NN = tagger.trigram_nnp_nnp_nn  # tri-grams with NNP + NNP + NN POS
        tf_idf_trigram_NNP_NN_NN = tagger.trigram_nnp_nn_nn  # tri-grams with NNP + NN + NN POS
        tf_idf_trigram_NN_NN_NN = tagger.trigram_nn_nn_nn  # tri-grams with NN + NN + NN POS
        tf_idf_trigram_NN_NNS_CD = tagger.trigram_nn_nns_cd  # tri-grams with NN + NNS + CD POS eg. clock cycles 8
        tf_idf_trigram_NN_NN_CD = tagger.trigram_nn_nn_cd  # tri-grams with NN + NN + CD POS eg. clock cycle 8

        # ------------ word bags Fourgrams -----------

        tf_idf_fourgram_NNP_NNP_NNP_NNP = tagger.fourgram_nnp_nnp_nnp_nnp  # fourgrams with NNP + NNP + NNP + NNP POS

        # ------------ word bags Fivegrams -----------
        # fivegrams with NNP + NNP + NNP + NNP + NNP POS
        tf_idf_fivegram_NNP_NNP_NNP_NNP_NNP = tagger.fivegram_nnp_nnp_nnp_nnp_nnp

        def neuro_fuzzy(x):
            range_span = RangeCalculator()
            range_span.calculate_filter_range(x)
            #tf_idf_values = range_span.tf_idf_values
            span = range_span.span
            span_pivots = range_span.pivots

            # ------------- Drawing Fuzzy & Scatter Plots --------------

            """
            draw_fuzzy = FuzzyPlotFilterI()
            draw_fuzzy.drawFuzzyPlotFilterI(tf_idf_values, span)
            draw_scatter = ScatterPlot()
            draw_scatter.drawScatterPlot(tf_idf_values)
            """

            # ------------- calculating DOM of fuzzy sets --------------

            dom = DegreeOfMembership()
            dom.find_fuzzy_set(x, span, span_pivots)
            y = dom.dom_data_list
            return y

            # ----------------------------------------------------------
        print 'Neuro-fuzzy ...'
        u1 = neuro_fuzzy(tf_idf_common_eng_words)
        u2 = neuro_fuzzy(tf_idf_nouns_unigrams)
        u3 = neuro_fuzzy(tf_idf_all_cap_unigrams)
        u4 = neuro_fuzzy(tf_idf_numbers_unigrams)

        # fuzzy sets for bigrams
        b1 = neuro_fuzzy(tf_idf_bigram_NNP_NNP)
        b2 = neuro_fuzzy(tf_idf_bigram_NNP_NN)
        b3 = neuro_fuzzy(tf_idf_bigram_NN_NN)
        b4 = neuro_fuzzy(tf_idf_bigram_NN_NNS)
        b5 = neuro_fuzzy(tf_idf_bigram_NN_VBD)

        # fuzzy sets for trigrams
        t1 = neuro_fuzzy(tf_idf_trigram_NNP_NNP_NNP)
        t2 = neuro_fuzzy(tf_idf_trigram_NNP_NNP_NN)
        t3 = neuro_fuzzy(tf_idf_trigram_NNP_NN_NN)
        t4 = neuro_fuzzy(tf_idf_trigram_NN_NN_NN)
        t5 = neuro_fuzzy(tf_idf_trigram_NN_NNS_CD)
        t6 = neuro_fuzzy(tf_idf_trigram_NN_NN_CD)

        # fuzzy sets for fourgrams
        f1 = neuro_fuzzy(tf_idf_fourgram_NNP_NNP_NNP_NNP)

        # fuzzy sets for fivegrams
        p1 = neuro_fuzzy(tf_idf_fivegram_NNP_NNP_NNP_NNP_NNP)  # p --> penta = five

        nf = NeuroFuzzySystem()
        nf.neuro_fuzzy_modelling(tf_idf_list, u1, u2, u3, u4,
                                 tf_idf_bigram_list,
                                 b1, b2, b3, b4, b5, tf_idf_trigram_list, t1, t2, t3, t4, t5, t6, tf_idf_fourgram_list,
                                 f1, tf_idf_fivegram_list, p1)

        nf.norm_cog_unigrams()
        nf.norm_cog_bigrams()
        nf.norm_cog_trigrams()
        nf.norm_cog_fourgrams()
        nf.norm_cog_fivegrams()

        PI_bundle_unigrams = nf.pi_bundle_unigrams
        PI_bundle_bigrams = nf.pi_bundle_bigrams
        PI_bundle_trigrams = nf.pi_bundle_trigrams
        PI_bundle_fourgrams = nf.pi_bundle_fourgrams
        PI_bundle_fivegrams = nf.pi_bundle_fivegrams

        # Exception try using assert
        if len(PI_bundle_unigrams) == 0 and len(PI_bundle_bigrams) == 0 and len(
                PI_bundle_trigrams) == 0 and len(
                PI_bundle_fourgrams) == 0 and len(PI_bundle_fivegrams) == 0:
            pass
        else:

            c = open('pi_sheet.csv', 'wb')
            csv_1 = csv.writer(c)
            csv_1.writerow(['Word', 'PI Score', 'Tf-Idf', 'Loc Ind'])

            for word, info in PI_bundle_unigrams.iteritems():
                csv_1.writerow([word, info[0], info[1][0], info[1][1]])
            for bigram, info in PI_bundle_bigrams.iteritems():
                csv_1.writerow([bigram, info[0], info[1][0], info[1][1]])
            for trigram, info in PI_bundle_trigrams.iteritems():
                csv_1.writerow([trigram, info[0], info[1][0], info[1][1]])
            for fourgram, info in PI_bundle_fourgrams.iteritems():
                csv_1.writerow([fourgram, info[0], info[1][0], info[1][1]])
            for fivegram, info in PI_bundle_fivegrams.iteritems():
                csv_1.writerow([fivegram, info[0], info[1][0], info[1][1]])

            c.close()

            # ******** Proximity Finder ********
            print 'Finding Proximity ...'

            file_1 = open('pi_sheet.csv', 'rU')
            csv_file_1 = csv.reader(file_1)
            file_2 = open('modified_pi_sheet.csv', 'wb')
            csv_file_2 = csv.writer(file_2)
            pf = ProximityFinder(csv_file_1, csv_file_2)
            pf.read_pi_sheet()
            pf.subsection_clustering()
            pf.build_distance_matrix()
            file_1.close()
            file_2.close()

            # ******** Concept Mining ********
            print 'Mining Concepts ...'

            file_3 = open('modified_pi_sheet.csv', 'rU')
            csv_file_3 = csv.reader(file_3)
            file_3_instance = open('modified_pi_sheet.csv', 'rU')
            csv_file_3_instance = csv.reader(file_3_instance)
            fc = FuzzyConcept(csv_file_3, csv_file_3_instance)
            fc.normalize_proximity_scores()
            file_3.close()
            file_4 = open('final_pi_sheet.csv', 'wb')
            csv_file_4 = csv.writer(file_4)
            fc.write_final_pi_sheet(csv_file_4)
            file_3_instance.close()
            file_4.close()
            file_5 = open('final_pi_sheet.csv', 'rU')
            csv_file_5 = csv.reader(file_5)
            fc.draw_concept_graphs(csv_file_5)
            file_5.close()

            pi_dict = fc.pi_dict
            ps_dict = fc.ps_dict

            # writing master PI and PS sheets
            ske = ConceptSkeleton(pi_dict, ps_dict, csv_out_1, csv_out_2)
            ske.write_output_to_csv()
            doc_file.close()

    out_1.close()
    out_2.close()

    # drawing master UAG
    master_uag = pgv.AGraph(directed=False, strict=True)
    f1 = open('PI.csv', 'rb')
    csv_f1 = csv.reader(f1)
    f2 = open('PS.csv', 'rb')
    csv_f2 = csv.reader(f2)
    uag = MasterUAG(csv_f1, csv_f2)
    uag.draw_master_uag(master_uag)
    uag.extract_concepts()
    concepts = uag.concepts

    f1.close()
    f2.close()

    #**************************************************************************************
    #                                   UAG to DAG
    #**************************************************************************************
    master_dag = pgv.AGraph(directed=True, strict=True)
    f1 = open('PI.csv', 'rb')
    csv_f1 = csv.reader(f1)
    f2 = open('PS.csv', 'rb')
    csv_f2 = csv.reader(f2)
    dag = MasterDAG(csv_f1, csv_f2, concepts)
    dag.create_dict()
    dag.draw_master_dag()
    d = pgv.AGraph(directed=True, strict=True)
    dag.construct_dac(d)