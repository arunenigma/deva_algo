import pygraphviz as pgv
from random import uniform
from itertools import product, tee, izip
import networkx as nx


class UAGtoDAG(object):
    def __init__(self, nodes, edges, th):
        self.nodes = nodes
        self.edges = edges
        self.th = th
        self.weighted_nodes = {}
        self.weighted_edges = {}
        self.rdf_triples = []

    def create_uag(self, uag):
        for node in self.nodes:
            self.weighted_nodes[node] = round(uniform(0.9, 1), 2)
        for edge in self.edges:
            self.weighted_edges[tuple(edge)] = round(uniform(0.8, 1), 2)

        for edge, ps in self.weighted_edges.iteritems():
            uag.add_node(edge[0], color='', style='filled', shape='box', xlabel=self.weighted_nodes.get(edge[0]),
                         font='')
            uag.add_node(edge[1], color='', style='filled', shape='box', xlabel=self.weighted_nodes.get(edge[0]),
                         font='')
            uag.add_edge(edge[0], edge[1], color='', style='', label=ps, fontname='')
        uag.write('uag.dot')
        img = pgv.AGraph(file='uag.dot')  # img = pgv.AGraph('graph.dot') doesn't work | bug in Pygraphviz
        img.layout(prog='dot')
        img.draw('uag.pdf')
        img.close()

    def uag_to_dag_algorithm(self, root):
        candidates = []
        validated_candidates = []
        children = []
        self.nodes.remove(root)
        search_node_pairs = product(root, self.nodes)
        for node_pair in list(search_node_pairs):
            if node_pair in self.weighted_edges.keys():
                cf = self.cf_case_1(node_pair)
                candidates.append([node_pair, round(cf, 2)])
            else:
                hidden_nodes = self.find_all_paths(node_pair[0], node_pair[1])[1:-1]
                if len(hidden_nodes) == 1:
                    cf = self.cf_case_2(node_pair[0], hidden_nodes[0], node_pair[1])
                    candidates.append([node_pair, round(cf, 2)])
                elif len(hidden_nodes) > 1:
                    cf = self.cf_case_3(node_pair[0], hidden_nodes, node_pair[1])
                    candidates.append([node_pair, round(cf, 2)])
        for candidate in candidates:
            if candidate[1] > self.th:
                validated_candidates.append(candidate)
        self.rdf_triples.append(validated_candidates)

        for candidate in validated_candidates:
            children.append(candidate[0][1])
        for node in children:
            self.nodes.remove(node)
        for child in children:
            self.nodes.append(child)
            self.uag_to_dag_algorithm(child)
        return self.rdf_triples

    def find_all_paths(self, ref_node, inspect_node):
        """
            iterative method to find all paths; given a reference and an inspection node
        """
        path = []
        paths = []
        uag = nx.Graph(self.edges)
        queue = [(ref_node, inspect_node, path)]
        while queue:
            start_node, end_node, path = queue.pop()
            path = path + [start_node]
            if start_node == end_node:
                paths.append(path)
            for node in set(uag[start_node]).difference(path):
                queue.append((node, end_node, path))
        return paths[0]

    def cf_case_1(self, pair):
        psi_r = self.weighted_nodes.get(pair[0])
        psi_i = self.weighted_nodes.get(pair[1])
        ps = self.weighted_edges.get((pair[0], pair[1]))
        if ps is None:
            ps = self.weighted_edges.get((pair[1], pair[0]))

        cf = ps * ((psi_r + psi_i) / 2)
        return cf

    def cf_case_2(self, ref, hid, ins):
        cf_1 = self.cf_case_1((ref, hid))
        cf_2 = self.cf_case_1((hid, ins))
        cf = cf_1 * cf_2
        return cf

    def cf_case_3(self, ref, hid, ins):
        cf_ref_h1 = self.cf_case_1((ref, hid[0]))
        cf_hl_ins = self.cf_case_1((hid[-1], ins))
        cf_hid = 1
        for pair in list(UAGtoDAG.pairwise(hid)):
            cf_hid *= self.cf_case_1(pair)
        cf = cf_ref_h1 * cf_hid * cf_hl_ins
        return cf

    @staticmethod
    def pairwise(lst):
        a, b = tee(lst)
        next(b, None)
        return izip(a, b)

    @staticmethod
    def construct_dac(validated_triples, dag):
        print validated_triples
        cleaned_rdf_triples = []
        edges = []
        for triples in validated_triples:
            for triple in triples:
                edges.append(triple[0])
                cleaned_rdf_triples.append([triple[0], triple[1]])

        for rdf_triple in cleaned_rdf_triples:
            print rdf_triple

        for edge in edges:
            dag.add_node(edge[0], color='', style='filled', shape='box',
                         font='')
            dag.add_node(edge[1], color='', style='filled', shape='box',
                         font='')
            dag.add_edge(edge[0], edge[1], color='', style='', fontname='')
        dag.write('dag.dot')
        img = pgv.AGraph(file='dag.dot')  # img = pgv.AGraph('graph.dot') doesn't work | bug in Pygraphviz
        img.layout(prog='dot')
        img.draw('dag.pdf')
        img.close()


if __name__ == '__main__':
    transform = UAGtoDAG(['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                         [['A', 'B'], ['A', 'E'], ['B', 'D'], ['A', 'C'], ['C', 'F'], ['D', 'G']],
                         0.6)
    u = pgv.AGraph(directed=False, strict=True)
    transform.create_uag(u)
    rdf_triples = filter(None, transform.uag_to_dag_algorithm('E'))
    d = pgv.AGraph(directed=True, strict=True)
    transform.construct_dac(rdf_triples, d)