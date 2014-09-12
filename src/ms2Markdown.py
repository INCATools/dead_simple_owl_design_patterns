import re


def hyperlink_quoted_entities(string, name_id, baseURI):
    """Hyperlink all quoted entities in 'string', rolling URIs using baseURI + name_id dict to look up shortForm IDs based on match to label"""
    # sub anything in quotes to ['label'](full_URI)
    owlMS_string = re.sub("\'.+?\'", (lambda m: "[" + m.group(1) + "]" + "(" + baseURI + name_id[m.group(1)]) + ")", owlMS_String)  # Perhaps should worry about word boundaries here?
       
def italic_keywords(owlMS_string):
    """Make MS keywords italic"""
    keywords = ("equivalentTo", "disjointWith", "subClassOf", "and", "that", "or", "some", "only", "not", "min", "max", "exactly") # Probably worth breaking this down further.
    # check for match to keyword and sub _keyword_
    for k in keywords:
        owlMS_string = re.sub(k, "_" + k + "_", owlMS_string) # TODO: Add word boundaries to match, also avoid matching inside quotes.
    return owlMS_string

def bold_relations(owlMS_string, relations):
    """Make relations bold.  Args: owlMS_string = OWL Manchester syntax string, all entities quoted; relations = list of relations"""
    for r in relations:
        owlMS_string = re.sub("(\'"+r"\')", "__" + r + "__", owl_MS_string)




