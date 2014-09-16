import re


def hyperlink_quoted_entities(string, name_id, baseURI):
    """Hyperlink all quoted entities in 'string', rolling URIs using baseURI + name_id dict to look up shortForm IDs based on match to label"""
    # sub anything in quotes to ['label'](full_URI)
    string = re.sub("\'(.+?)\'", lambda m: "[" + m.group(0) + "]" + "(" + baseURI + name_id[m.group(1)] + ")", string)  # Perhaps should worry about word boundaries here?
    return string
# test_hyperlink_quoted_entities():
assert hyperlink_quoted_entities("'abc' some 'xy z'", { "abc" : "123", "xy z": "456" }, "http://fu.bar/") == "['abc'](http://fu.bar/123) some ['xy z'](http://fu.bar/456)"
       
def italic_keywords(owlMS_string):
    """Make MS keywords italic"""
    keywords = ("equivalentTo", "disjointWith", "subClassOf", "and", "that", "or", "some", "only", "not", "min", "max", "exactly") # Probably worth breaking this down further.
    # check for match to keyword and sub _keyword_
    for k in keywords:
        owlMS_string = re.sub(r"\b%s\b" % k, "_" + k + "_", owlMS_string) # TODO: Add word boundaries to match, also avoid matching inside quotes.
    return owlMS_string

# italic keywords test
assert italic_keywords("equivalentTo disjointWith subClassOf and that or some only not min max exactly") ==  "_equivalentTo_ _disjointWith_ _subClassOf_ _and_ _that_ _or_ _some_ _only_ _not_ _min_ _max_ _exactly_"

def bold_relations(owlMS_string, relations):
    """Make relations bold.  Args: owlMS_string = OWL Manchester syntax string, all entities quoted; relations = list of relations"""
    for r in relations:
        owlMS_string = re.sub("(\'"+r+"\')", "__'" + r + "'__", owlMS_string)
    return owlMS_string

# bold relations test.
assert bold_relations("'abc' some 'xy z'", ["abc"]) == "__'abc'__ some 'xy z'"




