import warnings
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
    

class pattern:
    __metaclass__ = ABCMeta     # Abstract class - should not be directly instantiated

    # class level vars
    # pkey_dict spec. A dict of dicts.  keys are field names.  Subdicts have two compulsory boolan keys: compulsory & sprintf (indicating field will be paired with list and processed via sprintf subs).   If "compulsory" is False, there must be an additional boolean: oneOf, indicating whther this is one of a set, at least one of which must be present.  If sprintf is true, a further boolean, "msExpression", records whether the sprintf subfield 'string' is a Manchester syntax expression.
    
    pkey_dict = { "pattern_name" : { "compulsory" : True, "sprintf" : False }, "Description" : { "compulsory" : False, "OneOf" : False, "sprintf" : False }, "classes" : { "compulsory" : True, "sprintf" : False } , "relations" : { "compulsory" : True, "sprintf" : False }, "vars" :  { "compulsory" : True, "sprintf" : False }, "name" : { "compulsory" : True, "sprintf" : True, "msExpression" : False }, "def" : { "compulsory" : True, "sprintf" : True, "msExpression" : False}, "EquivalentTo" : { "compulsory" : False, "OneOf" : True, "sprintf" : True, "msExpression" : True }, "SubclassOf" : { "compulsory" : False, "OneOf" : True, "sprintf" : True, "msExpression" : True }, "GCI" : { "compulsory" : False, "OneOf" : False, "sprintf" : True, "msExpression" : True } }  # Better to specify this in JSON OR YAML in first place.  This is hard to read and edit.
    
    sprintf_keys = ("text", "vars")  # Perhaps embed this in pkey_dict.  Gives more scope for clearer names for fields. OTOH, code will be simpler with generic names.
    baseURI = "http://purl.obolibrary.org/obo/"  # Need this in separate config in order to make generic.


    #@abstractmethod
    def _validate_pattern_fields(self):
        # check pattern is dict ??

        # Iterate over pattern keys, check if valid,
        # Iterate over pkilst
        for key, value in self.pattern.items():
            if key not in self.pkey_dict:
                warnings.warn("Pattern has unknown field: %s !" % key)
        oneOf = False
        oneOf_list = []
        for key, value in self.pkey_dict.items():
            if value['compulsory']:
                if key not in self.pattern:
                    warnings.warn("Pattern is missing compulsory field: %s !" % key)
            elif value['OneOf']:
                oneOf_list.append(key)
                if key in self.pattern:
                    oneOf = True 
            if value['sprintf']:
                if key in self.pattern:
                    for key2 in self.pattern[key]:
                        if key2 not in self.sprintf_keys:
                            warnings.warn("The field %s has an uknown subfield %s." % (key, key2))
                    for key3 in self.sprintf_keys:
                        if key3 not in self.pattern[key]:
                            warnings.warn("The field %s lacks the compulsory subfield %s." % (key, key3))

        if not oneOf_list:
            warnings.warn("Pattern must have at least one of: " + str(oneOfList))

        # Poss to add: validate number of vars for sprintf subs

    def _validate_entities(self):
        # Check IDs are known/ non-obsolete
        for NAME, ID in self.pattern['classes'].items():
            if not self.ont.knowsClass(ID):
                warnings.warn("Pattern contains unknown class %s ; %s." % (NAME, ID))
        for NAME, ID in self.pattern['relations'].items():
            if not self.ont.knowsObjectProperty(ID):
                warnings.warn("Pattern contains unknown relation %s, %s." % (NAME, ID))
        # TODO - add check for obsoletion status

    def _validate_range(self):
        # Boolean check for classes in range class expression - may require a different reasoner.
        stub = 1

    def validate_abstract_pattern(self):
        self._validate_pattern_fields()
        self._validate_entities()

    def gen_name_id(self):
        name_id  = {}
        name_id.update(self.pattern['classes'])
        name_id.update(self.pattern['relations'])
        return name_id
    
    def _MS_name2Id(self, classExpression):
        # uses the list of entities in the pattern to sub all quoted entity names for IDs
        out = classExpression
        name_id = gen_name_id()
        for k, v in name_id.items():
            out = re.sub("\'"+k+"\'", v, out)  # Suspect this not Pythonic. Could probably be done with a fancy map lambda combo.  
        return out

    def _ms2md(self, msExpression):
        """Fully converts an msExpression to Markdown. Keywords -> italics; relations -> bold; entities -> hyperlinked."""
        print "before italic sub %s" % msExpression
        msExpression = ms2Markdown.italic_keywords(msExpression)
        print "after italic owl sub %s" % msExpression
        msExpression = ms2Markdown.bold_relations(msExpression, self.pattern['relations'].keys())
        print "after bold relation sub %s" % msExpression
        name_id = self.gen_name_id()
        msExpression = ms2Markdown.hyperlink_quoted_entities(msExpression, name_id, self.baseURI)
        return msExpression
        
    def _var_quote_sub(self, text, VARS):
        """Quotes all members of list VARS with {}, then uses the resulting list in sprintf sub with tartget 'text'"""
        ## No need to live on class.  Can be moved to tools.  - Add assert test.
        qvars = map(lambda x: "\{ " + x + " \}", VARS)
        return text % tuple(qvars)
        

class abstract_pattern(pattern):
    def __init__(self, pattern, ont):
       self.pattern = pattern # pattern python data structure
       self.ont = ont
       self.validate_abstract_pattern()

    def __string__(self):
            return str(self.pattern)

    def _ms_sub_and_md(self, fieldName):
        # Roll a list of {} quoted vars for sprintf field.  Use this in sub.
        l = []
        # for each var
        for v in self.pattern[fieldName]['vars']:
            l.append("{ " + v + " }") # roll a new list of vars, each deli
        ms_sub = self.pattern[fieldName]['text'] % tuple(l)
        return self._ms2md(ms_sub)

    def gen_markdown_doc(self):
        # Spec for markdown doc
        # vars displayed as \{ hyperlinked classExpression \}
        # pattern name
        # label rule
        # def
        # MS fields
        # dicts?

        # sprintf subs and MS conversion
        
        out = "## %s\n" % self.pattern['pattern_name'] #
        # sprintf to generate label  - Use { var name } in sub
        out += "__label:__ %s\n\n" % (self._var_quote_sub(self.pattern['name']['text'],self.pattern['name']['vars']))
        # sprintf to generate def - Use { var name } in sub
        out += "__def:__ %s\n\n" % (self._var_quote_sub(self.pattern['def']['text'],self.pattern['def']['vars']))
        
        if "EquivalentTo" in self.pattern:            
            out += "__equivalentTo:__ %s\n\n" % self._ms_sub_and_md('EquivalentTo')
        if "SubClassOf" in self.pattern:
            out += "__subClassOf:__ %s\n\n" % self._ms_sub_and_md('SubClassOf')
        if "GCI" in self.pattern:
            out += "__GCI:__ %s\n\n" % self._ms_sub_and_md('GCI')
        return out
        
    def update_entity_labels(self, ont):
        # This should report any changes, regenerate pattern.
        stub = 1

        
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

    def gen_markdown_doc():
        # spec: follow Manchester syntax
        stub = 1
    
    def validate_applied_pattern(self):
        _validate_var_entities()
        _has_subclasses()  # only needed for reporting purposes.

    def _validate_var_entities(self):
        stub = 1
            

    def _has_subclasses(self, ont):
        stub = 1
        # Boolean check for the presence of inferred subclasses.



        
