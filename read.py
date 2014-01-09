class ReadDocs(object):
    def __init__(self, docs):
        self.docs = docs

    def read_file(self, docs_file):
        i = 0
        docs = docs_file.read()

        if len(docs.strip()) > 0 and len(docs.split(' ')) > 2:
            if i < 100:
                self.docs.write('<xml>' + docs.strip() + '</xml>\n')
                i += 1
            else:
                #print 'TWEET ->', doc # doc entries that have missing fields
                pass
