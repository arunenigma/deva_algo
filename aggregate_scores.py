from itertools import groupby
from operator import itemgetter


class AggregateScores(object):
    def __init__(self, f1, f2, f3, f4):
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.f4 = f4
        self.pi = []
        self.ps = []

    def consolidate_pi_scores(self):
        for row in self.f1:
            word = row[0].lower()
            pi = float(row[1])
            self.pi.append([word, pi])
        self.pi.sort(key=itemgetter(0))
        for word, scores in groupby(self.pi, itemgetter(0)):
            scores = [pi[1] for pi in list(scores)]
            agg_pi = sum(scores)/float(len(scores))
            self.f3.writerow([word, agg_pi])

    def consolidate_ps_scores(self):
        for row in self.f2:
            pair = ((row[0].lower(), row[1].lower()))
            ps = float(row[2])
            self.ps.append([pair, ps])
        self.ps.sort(key=itemgetter(0))
        for pair, scores in groupby(self.ps, itemgetter(0)):
            scores = [ps[1] for ps in list(scores)]
            agg_ps = sum(scores) / float(len(scores))
            self.f4.writerow([pair[0], pair[1], agg_ps])