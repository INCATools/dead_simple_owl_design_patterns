import warnings
import yaml
import json
import ms2Markdown
from abc import ABCMeta, abstractmethod

# Two major requirements:
## testing and documentation of patterns
## testing, doc and implementation of instances
# Should these be split, or carried out by the same object? 

# For now, have made one abstract superclass and two subclasses - abstract and applied.  Usage-wise, this means a user could end up applying an invalid class... - will not be tested automatically.


# Pattern for turning a list, l in which the first arg is a sprintf statement and all subsequent args are the substitutions on that sprintf statement.
# def sprintf_sub(self, l):
#     return l[0] % tuple(map(lambda x: x.label, l[1:]))

def load_yaml(filePath):
    f = open (filePath, "r")
    yaml.load(f)

def load_json(filePath):
    f = open (filePath, "r")
    json.load(f)


def yaml2json(YamlfilePath, JsonFilePath):
    json.load(load_yaml(YamlfilePath))
    json.save(JsonFilePath)
    

class pattern:
    __metaclass__ = ABCMeta     # Abstract class - should not be directly instantiated

    # class level vars
    # pkey_dict spec. A dict of dicts.  keys are field names.  Subdicts have two compulsory boolan keys: compulsory & sprintf (indicating field will be paired with list and processed via sprintf subs).   If "compulsory" is False, there must be an additional boolean: oneOf, indicating whther this is one of a set, at least one of which must be present.  If sprintf is true, a further boolean, "msExpression", records whether the sprintf subfield 'string' is a Manchester syntax expression.
    
    self.pkey_dict = { "pattern_name" : { "compulsory" = True, "sprintf" = False } "classes" : { "compulsory" = True, "sprintf" = False } , "relations" : { "compulsory" = True, "sprintf" = False }, "vars" :  { "compulsory" = True, "sprintf" = False }, "name" : { "compulsory" = True, "sprintf" = True, "msExpression" = False }, "def" : { "compulsory" = True, "sprintf" = True, "msExpression" = False}, "EquivalentTo" : { "compulsory" = False, "OneOf = True, sprintf" = True, "msExpression" = True }, "SubclassOf" : { "compulsory" = False, "OneOf = True, sprintf" = True, "msExpression" = True }, "GCI" : { "compulsory" = False, "OneOf = False, sprintf" = True, "msExpression" = True } }  # Better to specify this in JSON OR YAML in first place.
    
    self.sprintf_keys = ("string", "vars")  # Perhaps embed this in pkey_dict.  Gives more scope for clearer names for fields. OTOH, code will be simpler with generic names.
    self.baseURI = "http://purl.obolibrary.org.obo/"  # Need this in separate config in order to make generic.

    #@abstractmethod
    def _validate_pattern_fields(self):
        # check pattern is dict ??

        # Iterate over pattern keys, check if valid,
        # Iterate over pkilst
        for key, value in self.pattern.items():
            if key not in self.pklist:
                warnings.warn("Pattern has unknown field: %s !" % key)
        oneOf = False
        oneOf_list = []
        for key, value in self.pklist.items():
            if value["compulsory"]:
                if key not in self.pattern:
                    warnings.warn("Pattern is missing compulsory field: %s !" % key)
            elif value["OneOf"]:
                oneOf_list.push(key)
                if key in self.pattern:
                    oneOf = True 
            if value["sprintf"]:
                if key in self.pattern:
                    for key2 in self.pattern[key]:
                        if key2 not in self.sprintf_keys:
                            warnings.warn("The field %s is missing compulsory subfield %s." % (key, key2))
        if not oneOf_list:
            warnings.warn("Pattern must have at least one of: " + str(oneOfList))

        # Poss to add: validate number of vars for sprintf subs

    def _validate_entities(self):
        # Check IDs are valid
        for c in self.pattern['classes']:
            if not self.ont.knowsClass(c):
                warnings.warn("Pattern contains unknown class %s" % c)
        for o in self.pattern['relations']:
            if not self.ont.knowsObjectProperty(o):
                warnings.warn("Pattern contains unknown relation")

    def _validate_range(self):
        # Boolean check for classes in range class expression - may require a different reasoner.
        stub = 1

    def validate_abstract_pattern(self):
        _validate_pattern_fields()
        _validate_entities()

    def gen_name_id(self):
        name_id  = {}
        name_id.update(self.classes)
        name_id.update(self.relations)
        return name_id
    
    def _MS_name2Id(self, classExpression):
        # uses the list of entities in the pattern to sub all quoted entity names for IDs
        out = classExpression
        name_id = gen_name_id()
        for k, v in name_id.items():
            out = re.sub("\'"+k+"\'", v, out)  # Suspect this not Pythonic. Could probably be done with a fancy map lambda combo.  
        return out

    def ms2md(self, msExpression):
        """Fully converts an msExpression to Markdown. Keywords -> italics; relations -> bold; entities -> hyperlinked."""
        ms2markdown.italic_keywords(msExpression)
        ms2markdown.bold_relations(msExpression, self.relations.keys())
        name = gen_name_id()
        ms2markdown.hyperlink_quoted_entities(msExpression, name_id, self.baseURI)
        


class abstract_pattern(pattern):
    def __init__(self, pattern, ont)
       self.pattern # pattern python data structure
       self.ont = ont
       self.validate_abstract_pattern()

    def __string__(self):
            return str(self.pattern)

    def gen_markdown_doc():
        ms_fields
        if equivalentTo in self.pattern:
            ec_md =
        if subClassOf
        sc_mf =
        gc_md = 
        # Spec for markdown doc
        # vars displayed as \{ hyperlinked classExpression \}  
        



        
class applied_pattern(pattern):

    def __init__(self, pattern, clist, ont):

       self.pattern = yaml.load(pattern) # better to use json and convert from yaml first?
       self.clist = clist  # Must be a list of name : ID tuples? - or dict?
       self.ont = ont
       self.validate_abstract_pattern(ont)  # important to check that pattern is safe to apply.
       self.validate_applied_pattern(ont)

    def __string__(self):
        # Return string should include subs 
        stub = 1

    def gen_markdown_doc

   

    ### Validation fns
    

    def _has_subclasses(self, ont):
        
        # Boolean check for the presence of inferred subclasses.

    def update_entity_labels(ont):
        # This should report any changes, regenerate pattern.
        stub = 1

# Push all these into an imported package.
# For testing:


        
