import csv


class DomainDictExtractor(object):
    def extractRelations(self):
        objs = {}
        feats = {}  # features includes synonyms | value -> relation and object
        attribs = {}

        fpu_dict = open('fpu.csv', 'rU')
        fpu_dict_csv = csv.reader(fpu_dict)
        fpu_dict_csv.next()

        attribs_exclude = ['text', 'number', 'yes', 'no']

        for row in fpu_dict_csv:
            objs[row[0].lower()] = 'is-an-object'
            # **************** features ***************
            if ',' in row[1]:
                features = row[1].split(',')
                for feature in features:
                    feats[feature.lower()] = str(row[3].lower()) + str(' of ') + str(row[0].lower())
            else:
                if len(row[2]) > 0:
                    feats[row[1].lower()] = str(row[3].lower()) + str(' of ') + str(row[0].lower())

            # **************** synonyms ***************
            if ',' in row[2]:
                synonyms = row[2].split(',')
                for synonym in synonyms:
                    feats[synonym.lower()] = str(row[3].lower()) + str(' of ') + str(row[0].lower())
            else:
                if len(row[2]) > 0:
                    feats[row[2].lower()] = str(row[3].lower()) + str(' of ') + str(row[0].lower())

            # **************** attributes ***************
            if ',' in row[5]:
                atts = row[5].split(',')
                for att in atts:
                    if not att in attribs_exclude:
                        if ',' in row[1]:
                            features = row[1].split(',')
                            for feature in features:
                                attribs[att.lower()] = 'is-an-attribute to ' + str(feature.lower())
                        else:
                                attribs[att.lower()] = 'is-an-attribute to ' + str(row[1].lower())
                        if ',' in row[2]:
                            synonyms = row[2].split(',')
                            for synonym in synonyms:
                                attribs[att.lower()] = 'is-an-attribute to ' + str(synonym.lower())
                        else:
                            if len(row[2]) > 0:
                                attribs[att.lower()] = 'is-an-attribute to ' + str(row[2].lower())

            else:
                if not row[5] in attribs_exclude:
                    if ',' in row[1]:
                        features = row[1].split(',')
                        for feature in features:
                            attribs[row[5].lower()] = 'is-an-attribute to ' + str(feature.lower())
                    else:
                        attribs[row[5].lower()] = 'is-an-attribute to ' + str(row[1].lower())
                    if ',' in row[2]:
                        synonyms = row[2].split(',')
                        for synonym in synonyms:
                            attribs[row[5].lower()] = 'is-an-attribute to ' + str(synonym.lower())
                    else:
                        if len(row[2]) > 0:
                            attribs[row[5].lower()] = 'is-an-attribute to ' + str(row[2].lower())
            # **************** attributes ***************

        return [objs, feats, attribs]