class ConceptSkeleton(object):
    def __init__(self, pi_dict, ps_dict, f1, f2):
        self.pi_dict = pi_dict
        self.ps_dict = ps_dict
        self.f1 = f1
        self.f2 = f2

    def write_output_to_csv(self):
        for node, pi in self.pi_dict.iteritems():
            self.f1.writerow([node, pi])
        for pair, ps_sect in self.ps_dict.iteritems():
            self.f2.writerow([pair[0], pair[1], ps_sect])