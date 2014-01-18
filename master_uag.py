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
        self.pi_dict = {}
        self.ps_dict = {}

        self.edges = []

    def draw_master_uag(self, ucg):
        for row in self.pi:
            self.pi_dict[row[0]] = row[1]

        print 'Drawing graph ...'
        for row in self.ps:
            self.ps_dict[tuple([row[0], row[1]])] = row[2]
            if len(row) == 3:  # invisible nodes DEFECT ?
                if row[0] != row[1]:
                    if self.remove_n_gram_cliche(row[0], row[1]) == 0:
                        # choosing words whose PI > 0.4 for reducing computations
                        if round(float(self.pi_dict.get(row[0])), 2) > 0.4 and round(float(self.pi_dict.get(row[1])),
                                                                                      2) > 0.4:
                            ucg.add_node(row[0], color='red', style='', shape='box',
                                         xlabel=round(float(self.pi_dict.get(row[0])), 2),
                                         fontname='courier')

                            ucg.add_node(row[1].lower(), color='red', style='', shape='box',
                                         xlabel=round(float(self.pi_dict.get(row[1])), 2),
                                         fontname='courier')

                            ucg.add_edge(row[0], row[1], color='blue', style='',
                                         label=round(float(row[2]), 2),
                                         fontname='courier')
        ucg.write('ucg.dot')
        u = pgv.AGraph(file='ucg.dot')
        u.layout(prog='dot')

        # Building UCG from UAG cleverly. Transforming is computational more expensive I guess!
        # love Python
        edges = u.edges()
        self.edges = edges
        uag = pgv.AGraph(directed=False, strict=True)
        for edge in edges:
            if not edge[1] in u.predecessors(edge[0]):
                if self.ucg_to_uag_helper(u, edge[0], edge[1]) is True:
                    uag.add_node(edge[0], color='red', style='', shape='box',
                                 xlabel=round(float(self.pi_dict.get(edge[0])), 2),
                                 fontname='courier')

                    uag.add_node(edge[1].lower(), color='red', style='', shape='box',
                                 xlabel=round(float(self.pi_dict.get(edge[1])), 2),
                                 fontname='courier')

                    uag.add_edge(edge[0], edge[1], color='blue', style='',
                                 label=round(float(self.ps_dict.get((edge[0], edge[1]))), 2),
                                 fontname='courier')

        uag.write('uag.dot')
        u = pgv.AGraph(file='uag.dot')
        u.layout(prog='dot')
        u.draw('uag.pdf')

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

    def ucg_to_uag_helper(self, uag, n1, n2):
        ancestors = uag.predecessors(n1)
        n2_edges = list(itertools.product([n2], ancestors))
        print n2, n2_edges
        flag = True
        reversed_n2_edges = []
        for n2_edge in n2_edges:
            reversed_n2_edges.append(tuple(reversed(n2_edge)))
        n2_edges += reversed_n2_edges
        for n2_edge in n2_edges:
            if n2_edge in self.edges:
                flag = False
                break
        return flag

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