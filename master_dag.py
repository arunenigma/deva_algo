import csv
from itertools import product, tee, izip
from operator import itemgetter
import pygraphviz as pgv
import networkx as nx


class Memoize(object):
    # using class as a decorator
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = self.func(*args)
        return self.cache[args]


class MasterDAG(object):
    def __init__(self, pi, ps, concepts, doc_name):
        self.pi = pi
        self.ps = ps
        self.concepts = concepts
        self.pi_dict = {}
        self.ps_dict = {}
        self.nodes = []
        self.edges = []
        self.th = 0
        self.rdf_triples = []
        self.root_node = ''
        self.dag_nodes = []
        self.dag_edges = []
        self.computation = 0
        self.dag = {}
        self.doc_name = doc_name  # chapter number

    def create_dict(self):
        for row in self.pi:
            self.pi_dict[row[0]] = row[1]
        for row in self.ps:
            self.ps_dict[tuple([row[0], row[1]])] = row[2]
        for nodes, edges in self.concepts.iteritems():
            self.nodes.append(nodes)
            self.edges.append(edges)

    def draw_master_dag(self):
        for nodes, edges in zip(self.nodes, self.edges):
            candidates = []
            # fixing the root as the node with maximum PI
            for node in nodes:
                if not self.pi_dict.get(node) is None:
                    candidates.append([node, self.pi_dict.get(node)])
            candidates = sorted(candidates, key=itemgetter(1))
            self.root_node = candidates[-1][0]
            self.dag_nodes = nodes
            self.dag_edges = edges
            self.uag_to_dag_algorithm(self, self.root_node)

    @Memoize
    def uag_to_dag_algorithm(self, root):
        print 'UAG to DAG conversion'
        self.dag_nodes = list(self.dag_nodes)
        candidates = []
        validated_candidates = []
        children = []
        self.dag_nodes.remove(root)
        search_node_pairs = list(product([root], self.dag_nodes))
        for node_pair in search_node_pairs:
            if node_pair in self.ps_dict.keys() or tuple(reversed(node_pair)) in self.ps_dict.keys():
                print 'CF 1'
                cf = self.cf_case_1(node_pair)
                candidates.append([node_pair, round(cf, 2)])
            else:
                print 'CF 2 or 3'
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
            self.dag_nodes.remove(node)
        for child in children:
            self.dag_nodes.append(child)
            self.uag_to_dag_algorithm(self, child)

    def find_all_paths(self, ref_node, inspect_node):
        """
            iterative method to find all paths; given a reference and an inspection node
        """
        print 'finding paths'
        self.computation += 1
        print 'uag to dag ..', self.computation
        path = []
        paths = []
        dag = nx.Graph(self.dag_edges)
        queue = [(ref_node, inspect_node, path)]
        while queue:
            start_node, end_node, path = queue.pop()
            path = path + [start_node]
            if start_node == end_node:
                paths.append(path)
            for node in set(dag[start_node]).difference(path):
                queue.append((node, end_node, path))
        return paths[0]

    def cf_case_1(self, pair):
        print pair
        psi_r = float(self.pi_dict.get(pair[0]))
        psi_i = float(self.pi_dict.get(pair[1]))
        ps = self.ps_dict.get((pair[0], pair[1]))
        if ps is None:
            ps = self.ps_dict.get((pair[1], pair[0]))

        cf = float(ps) * ((psi_r + psi_i) / 2.0)
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
        for pair in list(self.pairwise(hid)):
            cf_hid *= self.cf_case_1(pair)
        cf = cf_ref_h1 * cf_hid * cf_hl_ins
        return cf

    @staticmethod
    def pairwise(lst):
        a, b = tee(lst)
        next(b, None)
        return izip(a, b)

    def construct_dac(self, dag):
        print 'cleaning RDF triples'
        cleaned_rdf_triples = []
        edges = []
        for triples in self.rdf_triples:
            for triple in triples:
                if triple:
                    edges.append([triple[0], triple[1]])
                    cleaned_rdf_triples.append([triple[0][0], triple[0][1], triple[1]])

        dag_csv = str(self.doc_name) + '.csv'
        cf_file = open('./dot/' + dag_csv, 'wb')
        cf = csv.writer(cf_file)
        for edge in edges:
            if self.remove_n_gram_cliche(edge[0][0], edge[0][1]) == 0:
                w1 = edge[0][0]
                w2 = edge[0][1]
                cf.writerow([w1, w2, edge[1]])
                dag.add_node(w1, color='red', style='', shape='box',
                             fontname='courier')
                dag.add_node(w2, color='red', style='', shape='box',
                             fontname='courier')
                dag.add_edge(w1, w2, color='blue', style='', fontname='',
                             xlabel=edge[1])

        dag_name = str(self.doc_name) + '.dot'
        dag.write('./dot/' + dag_name)
        g = pgv.AGraph(file='./dot/' + dag_name)  # img = pgv.AGraph('graph.dot') doesn't work | bug in Pygraphviz
        g.layout(prog='dot')
        self.dag = str(g)  # dot string passed to graph search class
        g.close()
        cf_file.close()

    @staticmethod
    def remove_n_gram_cliche(node_1, node_2):
        if len(node_1.split(' ')) < len(node_2.split(' ')):
            inter = dict.fromkeys([x for x in node_1.split(' ') if x in node_2.split(' ')])
            return len(inter)
        else:
            inter = dict.fromkeys([x for x in node_2.split(' ') if x in node_1.split(' ')])
            return len(inter)