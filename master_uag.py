import itertools
import pygraphviz as pgv
import networkx as nx


class MasterUAG(object):
    def __init__(self, pi, ps):
        self.pi = pi
        self.ps = ps
        self.inference_paths = []
        self.skeletons = []
        self.concepts = {}

    def draw_master_uag(self, uag):
        print 'Drawing graph ...'
        for row in self.ps:
            if len(row) == 3:  # invisible nodes DEFECT ?
                if row[0] != row[1]:
                    if self.remove_n_gram_cliche(row[0], row[1]) == 0:
                        uag.add_node(row[0], color='red', style='', shape='box',
                                     xlabel=round(float(0.0), 2),
                                     fontname='courier')

                        uag.add_node(row[1].lower(), color='red', style='', shape='box',
                                     xlabel=round(float(0.0), 2),
                                     fontname='courier')

                        uag.add_edge(row[0], row[1], color='blue', style='',
                                     label=round(float(row[2]), 2),
                                     fontname='courier')
        uag.write('uag.dot')
        u = pgv.AGraph(file='uag.dot')
        u.layout(prog='dot')
        u.draw('concepts.pdf')

        edges = u.edges()
        g1 = nx.Graph(edges)
        self.skeletons = nx.connected_components(g1)[:]

        for skeleton in self.skeletons:
            paths = []
            pairs = list(itertools.combinations(skeleton, 2))
            for pair in pairs:
                for edge in edges:
                    if pair == edge:
                        paths.append(pair)
                    if tuple(reversed(pair)) == edge:
                        paths.append(tuple(reversed(pair)))
            self.inference_paths.append(paths)

    @staticmethod
    def remove_n_gram_cliche(node_1, node_2):
        if len(node_1.split(' ')) < len(node_2.split(' ')):
            inter = dict.fromkeys([x for x in node_1.split(' ') if x in node_2.split(' ')])
            return len(inter)
        else:
            inter = dict.fromkeys([x for x in node_2.split(' ') if x in node_1.split(' ')])
            return len(inter)

    def extract_concepts(self):
        for skeleton, paths in zip(self.skeletons, self.inference_paths):
            if not len(paths) == 0:
                self.concepts[tuple(skeleton)] = paths
            else:
                self.concepts[tuple(skeleton)] = [tuple(skeleton)]