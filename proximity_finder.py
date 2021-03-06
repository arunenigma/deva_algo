#!/usr/bin/env python
from math import fabs, log10
import numpy as np


class ProximityFinder(object):
    def __init__(self, f1, f2):
        """
        @param f1: PI sheet
        @param f2: Modified PI Sheet with PS
        """
        self.f1 = f1
        self.f2 = f2
        self.f2.writerow(
            ['Feature Word', 'Priority Index Old', 'Proximity Score', 'Neighbour'])
        self.section_n_grams = []
        self.heads = []
        self.head_clusters = {}

        # unstructured text
        self.tails = []
        self.tail_clusters = {}

    def read_pi_sheet(self):
        self.f1.next()
        for row in self.f1:
            # unigrams
            if len(row[0].split(' ')) == 1 and not '|' in row[3]:
                start_head = str(sum([int(i) for i in row[3].split(' ')[:-2]])) + ' | ' + str(
                    len([int(i) for i in row[3].split(' ')[:-2]]))
                start_tail = [int(i) for i in row[3].split(' ')[-2:]]
                self.section_n_grams.append([row[0], row[1], start_head, start_tail])

            if len(row[0].split(' ')) == 2 and row[3].count('|') == 1:
                start_head = str(sum([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]])) + ' | ' + str(
                    len([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]]))
                start_tail = [int(i) for i in row[3].split(' | ')[0].split(' ')[-2:]]
                end_head = sum([int(i) for i in row[3].split(' | ')[1].split(' ')[:-2]])
                end_tail = [int(i) for i in row[3].split(' | ')[1].split(' ')[-2:]]
                self.section_n_grams.append(
                    [row[0], row[1], start_head, start_tail, end_head, end_tail])

            if len(row[0].split(' ')) == 3 and row[3].count('|') == 2:
                start_head = str(sum([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]])) + ' | ' + str(
                    len([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]]))
                start_tail = [int(i) for i in row[3].split(' | ')[0].split(' ')[-2:]]
                end_head = sum([int(i) for i in row[3].split(' | ')[2].split(' ')[:-2]])
                end_tail = [int(i) for i in row[3].split(' | ')[2].split(' ')[-2:]]
                self.section_n_grams.append(
                    [row[0], row[1], start_head, start_tail, end_head, end_tail])

            if len(row[0].split(' ')) == 4 and row[3].count('|') == 3:
                start_head = str(sum([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]])) + ' | ' + str(
                    len([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]]))
                start_tail = [int(i) for i in row[3].split(' | ')[0].split(' ')[-2:]]
                end_head = sum([int(i) for i in row[3].split(' | ')[3].split(' ')[:-2]])
                end_tail = [int(i) for i in row[3].split(' | ')[3].split(' ')[-2:]]
                self.section_n_grams.append(
                    [row[0], row[1], start_head, start_tail, end_head, end_tail])

            if len(row[0].split(' ')) == 5 and row[3].count('|') == 4:
                start_head = str(sum([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]])) + ' | ' + str(
                    len([int(i) for i in row[3].split(' | ')[0].split(' ')[:-2]]))
                start_tail = [int(i) for i in row[3].split(' | ')[0].split(' ')[-2:]]
                end_head = sum([int(i) for i in row[3].split(' | ')[4].split(' ')[:-2]])
                end_tail = [int(i) for i in row[3].split(' | ')[4].split(' ')[-2:]]
                self.section_n_grams.append(
                    [row[0], row[1], start_head, start_tail, end_head, end_tail])

    """
    structured text
    def subsection_clustering(self):
        for ngram in self.section_n_grams:
            self.heads.append(ngram[2])
        self.heads = list(set(self.heads))

        for head in self.heads:
            head_cluster = []
            for ngram in self.section_n_grams:
                if head == ngram[2]:
                    head_cluster.append(ngram)
            self.head_clusters[head] = head_cluster
    """

    def subsection_clustering(self):
        """
        clustering of unstructured text
        clustering is done based on statement number
        for structured text it is done based on section and subsections
        """
        for ngram in self.section_n_grams:
            self.tails.append(ngram[3][0])
        self.tails = list(set(self.tails))

        for tail in self.tails:
            tail_cluster = []
            for ngram in self.section_n_grams:
                if tail == ngram[3][0]:
                    tail_cluster.append(ngram)
            self.tail_clusters[tail] = tail_cluster

    def build_distance_matrix(self):
        print 'Building Distance Matrices ...'
        # for unstructured text, distance matrices are created for every single statement
        for tail, ngrams in self.tail_clusters.iteritems():
            word_indices = []
            stmt_indices = []
            priority_indices = []
            feature_words = []
            dm_w_rows = []
            dm_s_rows = []
            dm_p_rows = []

            for ngram in ngrams:
                word_indices.append(ngram[3][1])
                stmt_indices.append(ngram[3][0])
                priority_indices.append(ngram[1])
                feature_words.append(ngram[0])

            word_indices_clone = word_indices
            stmt_indices_clone = stmt_indices
            priority_indices_clone = priority_indices
            for word_index, stmt_index, priority_index in zip(word_indices, stmt_indices, priority_indices):
                dm_w_row = []
                #dm_s_row = [] # All statement info is commented out for unstructured text
                dm_p_row = []
                for word_index_clone, stmt_index_clone, priority_index_clone in zip(word_indices_clone,
                                                                                    stmt_indices_clone,
                                                                                    priority_indices_clone):
                #if word_index != word_index_clone: will FAIL because diagonal as 0's are needed for np array
                # TypeError: Iterator REFS_OK flag was not enabled will happen when trying to nditer below
                # math computation refer ICTAI 2013 NEFCIS
                    dm_w_row.append(
                        fabs((1 + word_index) - (1 + word_index_clone)))
                    #dm_s_row.append(fabs((1 + stmt_index) - (1 + stmt_index_clone)))
                    dm_p_row.append(fabs(float(priority_index) - float(priority_index_clone)))
                dm_w_rows.append(dm_w_row)
                #dm_s_rows.append(dm_s_row)
                dm_p_rows.append(dm_p_row)
            dm_w = np.array(dm_w_rows)
            #dm_s = np.array(dm_s_rows)
            dm_p = np.array(dm_p_rows)
            prox_mat = []
            #n_s = len(np.unique(dm_s))
            n_w = dm_w.shape[0]

            """
            for w_dist, s_dist, PI in zip(np.nditer(dm_w), np.nditer(dm_s), np.nditer(dm_p)):
                if PI == 0.0:
                    proximity_score = (w_dist + (n_s * s_dist)) / (n_w * n_s)
                    prox_mat.append(proximity_score)
                else:
                    proximity_score = ((w_dist + (n_s * s_dist)) / (
                        n_w * n_s)) * log10(10 * PI)
                    prox_mat.append(proximity_score)
            """
            for w_dist, PI in zip(np.nditer(dm_w), np.nditer(dm_p)):
                if PI == 0.0:
                    proximity_score = w_dist / n_w
                    prox_mat.append(proximity_score)
                else:
                    proximity_score = (w_dist / n_w) * log10(10 * PI)
                    prox_mat.append(proximity_score)

            ps = np.array(prox_mat)
            ps = np.reshape(ps, dm_w.shape)
            for r, row in enumerate(ps):
                if len(row) > 1:
                    row_clone = row
                    np.ndarray.sort(row)  # sort to catch the minimum other than 0
                    m = row[1]
                    for i, ele in enumerate(row_clone):
                        if ele == m:
                            self.f2.writerow(
                                [feature_words[r], priority_indices[r], 1 - m, feature_words[i]])