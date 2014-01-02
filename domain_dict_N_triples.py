import csv
import pygraphviz as pgv

f = open('fpu.csv', 'rU')
csv_f = csv.reader(f)
csv_f.next()
N_triples = []
for row in csv_f:
    N_triples.append((row[1], row[3], row[0]))
graph = pgv.AGraph(directed=False, strict=True)
for triple in N_triples:
    graph.add_node(triple[0].lower(), color='goldenrod2', style='filled', shape='box',
                   fontname='calibri')
    graph.add_node(triple[2].lower(), color='goldenrod2', style='filled', shape='box',
                   fontname='calibri')
    graph.add_edge(triple[0].lower(), triple[2].lower(), color='sienna', style='filled', label=triple[1].lower(),
                   fontname='calibri')
graph.write('dd_graph.dot')
img = pgv.AGraph(file='dd_graph.dot')
img.layout(prog='dot')
img.draw('dd_ontology.pdf')
img.close()
