import csv
import fnmatch
import os
import pygraphviz as pgv
import networkx as nx


class GraphSearch(object):
    def __init__(self, dot, cf_map, dot_name):
        self.dag = dot
        self.cf_map = cf_map
        self.stmts = []
        self.matched_ancestors = []
        self.matched_children = []
        self.results = {}
        self.cf = {}
        self.cf_normalized = {}
        self.dot_name = dot_name
        self.edges = []

    def draw_dags(self):
        for row in self.cf_map:
            self.cf[(row[0], row[1])] = float(row[2])
        max_cf = max(self.cf.values())
        for pair, con_fac in self.cf.iteritems():
            self.cf_normalized[(pair[0], pair[1])] = con_fac / max_cf

        dag = pgv.AGraph(directed=False, strict=True)
        d = dag.from_string(self.dag)
        self.edges = d.edges()
        for edge in self.edges:
            dag.add_node(edge[0], color='red', style='', shape='box',
                         fontname='courier')
            dag.add_node(edge[1], color='red', style='', shape='box',
                         fontname='courier')
            dag.add_edge(edge[0], edge[1], color='blue', style='', fontname='',
                         xlabel=round(self.cf_normalized.get((edge[0], edge[1])), 2))
        name = self.dot_name.replace('.dot', '.pdf')
        dag.write(self.dot_name)
        u = pgv.AGraph(file=self.dot_name)
        u.layout(prog='dot')
        u.draw(name)

    def ancestry(self, q):
        q_kw = q.split(' ')
        dag = pgv.AGraph(directed=False, strict=True)
        d = dag.from_string(self.dag)
        edges = d.edges()
        #print edges
        for edge in edges:
            for kw in q_kw:
                if kw == edge[0]:
                    print 'Match Found: ', edge, list(reversed(self.get_predecessors(d, edge[0]))), d.successors(
                        edge[0])
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
                    print 'Match Found: ', edge, list(reversed(self.get_predecessors(d, edge[1]))), self.get_successors(
                        d, edge[1])
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
        for document in self.recurse_dir(r'./epics', '*.txt'):
            document_file = open(document, 'rb')
            document = document_file.read()
            for stmt in document.split('. '):
                self.stmts.append(stmt)
            document_file.close()

    @staticmethod
    def recurse_dir(path, file_type):
        for r, directory, documents in os.walk(path):
            for document in fnmatch.filter(documents, file_type):
                yield os.path.join(r, document)

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
    query = raw_input('Enter search query: ')
    for root, dirs, docs in os.walk('./'):
        for doc in docs:
            if 'dag' in doc and '.dot' in doc:
                dag_dot = open(doc, 'rb').read()
                cf_file = open(doc.replace('.dot', '.csv'), 'rb')
                cf = csv.reader(cf_file)
                search = GraphSearch(dag_dot, cf, doc)
                search.draw_dags()
                #
                search.ancestry(query)
                search.get_statements()
                search.all_lower_case()
                search.match_stmts()
                search.print_results()