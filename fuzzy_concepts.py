import pygraphviz as pgv
import networkx as nx
import itertools


class FuzzyConcept(object):
    def __init__(self, f1, f1_clone):
        self.f1 = f1
        self.f1_clone = f1_clone
        self.pi_dict = {}
        self.ps_dict = {}

        self.header = ''

        self.max_pi = 0.0
        self.min_pi = 0.0
        self.max_ps = 0.0
        self.denum = 0.0

        self.skeletons = []
        self.inference_paths = []

    def normalize_proximity_scores(self):
        ps = []
        pi = []
        self.header = self.f1.next()

        for row in self.f1:
            pi.append(float(row[1]))
            ps.append(float(row[2]))
        print ps
        self.max_ps = max(ps)
        self.min_pi = min(pi)
        self.max_pi = max(pi)
        self.denum = self.max_pi - self.min_pi

    def write_final_pi_sheet(self, f2):
        self.pi_dict = {}
        f2.writerow(self.header)
        self.f1_clone.next()
        for row in self.f1_clone:
            if not self.max_pi == self.min_pi:
                f2.writerow(
                    [row[0], (float(row[1]) - self.min_pi) / self.denum, float(row[2]) / self.max_ps, row[3]])
                self.pi_dict[row[0]] = (float(row[1]) - self.min_pi) / self.denum
            else:
                f2.writerow([row[0], (float(row[1])), float(row[2]), row[3]])
                self.pi_dict[row[0]] = (float(row[1]))

    def draw_concept_graphs(self, f3, graph):
        f3.next()
        for row in f3:
            # converting all strings to lower case
            self.pi_dict[row[0].lower()] = row[1].lower()
            self.ps_dict[tuple([row[0].lower(), row[3].lower()])] = row[2]

            graph.add_node(row[0].lower(), color='', style='', shape='box',
                           xlabel=round(float(row[1]), 2),
                           fontname='')
            graph.add_node(row[3].lower(), color='', style='', shape='box',
                           xlabel=round(float(row[1]), 2),
                           fontname='')

            if not row[0].lower() is row[3].lower():
                graph.add_edge(row[0].lower(), row[3].lower(), color='', style='',
                               label=round(float(row[2]), 2),
                               fontname='')