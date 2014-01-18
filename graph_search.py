import csv
import fnmatch
import os
import pygraphviz as pgv
import networkx as nx


class GraphSearch(object):
    def __init__(self, dot, cf_map):
        self.dag = dot
        self.cf_map = cf_map
        self.stmts = []
        self.matched_ancestors = []
        self.matched_children = []
        self.results = {}
        self.cf = {}

    def create_cf_map(self):
        for row in self.cf_map:
            self.cf[(row[0], row[1])] = row[2]

    def ancestry(self, q):
        q_kw = q.split(' ')
        dag = pgv.AGraph(directed=False, strict=True)
        d = dag.from_string(self.dag)
        edges = d.edges()
        for edge in edges:
            for kw in q_kw:
                if kw == edge[0]:
                    print 'Match Found: ', edge, list(reversed(self.get_predecessors(d, edge[0]))), d.successors(edge[0])
                    print
                    ancestors = list(reversed(self.get_predecessors(d, edge[0])))
                    ancestors.append(edge[0])
                    if not ancestors in self.matched_ancestors:
                        self.matched_ancestors.append(ancestors)

                    children = list(reversed(self.get_successors(d, edge[0])))
                    children.append(edge[0])
                    if not children in self.matched_children:
                        self.matched_children.append(children)

                elif kw == edge[1]:
                    print 'Match Found: ', edge, list(reversed(self.get_predecessors(d, edge[1]))), self.get_successors(d, edge[1])
                    print
                    ancestors = list(reversed(self.get_predecessors(d, edge[1])))
                    ancestors.append(edge[1])
                    if not ancestors in self.matched_ancestors:
                        self.matched_ancestors.append(ancestors)

                    children = list(reversed(self.get_successors(d, edge[1])))
                    children.append(edge[1])
                    if not children in self.matched_children:
                        self.matched_children.append(children)
                else:
                    pass

    @staticmethod
    def get_predecessors(d, n):
        ancestors = []
        while d.predecessors(n):
            for ancestor in d.predecessors(n):
                ancestors.append(ancestor)
            n = d.predecessors(n)[0]
        return ancestors

    @staticmethod
    def get_successors(d, n):
        children = []
        while d.successors(n):
            for ancestor in d.successors(n):
                children.append(ancestor)
            n = d.successors(n)[0]
        return children

    def get_statements(self):
        for doc in self.recurse_dir(r'./epics', '*.txt'):
            doc_file = open(doc, 'rb')
            doc = doc_file.read()
            for stmt in doc.split('. '):
                self.stmts.append(stmt)
            doc_file.close()

    @staticmethod
    def recurse_dir(path, file_type):
        for root, dirs, docs in os.walk(path):
            for document in fnmatch.filter(docs, file_type):
                yield os.path.join(root, document)

    def all_lower_case(self):
        stmts = []
        for stmt in self.stmts:
            stmt = [w.lower() for w in stmt.split(' ')]
            stmts.append(stmt)
        self.stmts = stmts

    def match_stmts(self):
        for stmt in self.stmts:
            for item in self.matched_ancestors + self.matched_children:
                match = set(stmt).intersection(set(item))
                query_kw = item[-1]
                if query_kw in match:
                    self.results[tuple(match)] = ' '.join(stmt)

    def print_results(self):
        for match, stmt in self.results.iteritems():
            print 'MATCH:', match
            print
            print stmt
            print '**************************************************************************\n'

if __name__ == '__main__':
    dag_dot = open('dag.dot', 'rb').read()
    cf_file = open('cf.csv', 'rb')
    cf = csv.reader(cf_file)
    search = GraphSearch(dag_dot, cf)
    query = raw_input('Enter search query: ')
    search.ancestry(query)
    search.get_statements()
    search.all_lower_case()
    search.match_stmts()
    search.print_results()