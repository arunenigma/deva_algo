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
        self.min_ps = 0.0
        self.denum = 0.0
        self.denum_ps = 0.0

        self.skeletons = []
        self.inference_paths = []

    def normalize_proximity_scores(self):
        ps = []
        pi = []
        self.header = self.f1.next()

        for row in self.f1:
            print row
            pi.append(float(row[1]))
            ps.append(float(row[2]))
        self.max_ps = max(ps)
        self.min_ps = min(ps)
        self.min_pi = min(pi)
        self.max_pi = max(pi)
        self.denum = self.max_pi - self.min_pi
        self.denum_ps = self.max_ps - self.min_ps

    def write_final_pi_sheet(self, f2):
        self.pi_dict = {}
        f2.writerow(self.header)
        self.f1_clone.next()
        for row in self.f1_clone:
            if not self.max_pi == self.min_pi:
                f2.writerow(
                    [row[0], (float(row[1]) - self.min_pi) / self.denum, (float(row[2]) - self.min_ps) / self.denum_ps, row[3]])
                self.pi_dict[row[0]] = (float(row[1]) - self.min_pi) / self.denum
            else:
                f2.writerow([row[0], (float(row[1])), float(row[2]), row[3]])
                self.pi_dict[row[0]] = (float(row[1]))

    def draw_concept_graphs(self, f3):
        f3.next()
        for row in f3:
            # converting all strings to lower case
            self.pi_dict[row[0].lower()] = row[1].lower()
            self.ps_dict[tuple([row[0].lower(), row[3].lower()])] = row[2]
