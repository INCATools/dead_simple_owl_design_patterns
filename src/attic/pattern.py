import warnings
import ms2Markdown
import re
import json
from abc import ABCMeta#, abstractmethod

# Two major requirements:
## testing and documentation of patterns
## testing, doc and implementation of instances


# For now, have made one abstract superclass and two subclasses - abstract and applied.  Usage-wise, this means a user could end up applying an invalid class... - will not be tested automatically.

def load_json_from_file(path):
    """Loads json from specified file. Returns the corresponding data structure.
    """
    
    json_file = open(path, "r")
    json_string = json_file.read()
    json_file.close()
    return json.loads(json_string)

def gen_applied_pattern_from_json(path, dc, ont):
    """Returns and applied pattern object 
    """
    pattern = load_json_from_file(path)
    return applied_pattern(pattern, dc, ont)

class metaPattern:
    __metaclass__ = ABCMeta     # Abstract class - should not be directly instantiated

    # class level vars
    # pkey_dict spec. A dict of dicts.  keys are field names.  Subdicts have two compulsory boolean keys: compulsory & sprintf (indicating field will be paired with list and processed via sprintf subs).   If "compulsory" is False, there must be an additional boolean: oneOf, indicating whther this is one of a set, at least one of which must be present.  If sprintf is true, a further boolean, "msExpression", records whether the sprintf subfield 'string' is a Manchester syntax expression.
    
    pkey_dict = { "pattern_name" : { "compulsory" : True, "sprintf" : False },
                "Base_URI" : {"compulsory" : False, "OneOf" : False, "sprintf" : False},
                "Description" : { "compulsory" : False, "OneOf" : False, "sprintf" : False },
                "classes" : { "compulsory" : True, "sprintf" : False } ,
                "relations" : { "compulsory" : True, "sprintf" : False },
                "vars" :  { "compulsory" : True, "sprintf" : False },
                "name" : { "compulsory" : True, "sprintf" : True, "msExpression" : False },
                "def" : { "compulsory" : True, "sprintf" : True, "msExpression" : False}, 
                "comment" : { "compulsory" : False, "OneOf" : False,"sprintf" : True, "msExpression" : False },
                "equivalentTo" : { "compulsory" : False, "OneOf" : True, "sprintf" : True, "msExpression" : True }, 
                "subClassOf" : { "compulsory" : False, "OneOf" : True, "sprintf" : True, "msExpression" : True }, 
                "GCI" : { "compulsory" : False, "OneOf" : False, "sprintf" : True, "msExpression" : True } }  # Better to specify this in JSON OR YAML in first place.  This is hard to read and edit.
    
    sprintf_keys = ("text", "vars")  # Perhaps embed this in pkey_dict.  Gives more scope for clearer names for fields. OTOH, code will be simpler with generic names.
    baseURI = "http://purl.obolibrary.org/obo/"  # Need this in separate config in order to make generic.


    def _validate_pattern_fields(self):
        """Checks if all field and subfield keys are valid and if all compulsory fields are present"""
        # TO ADD:
        ## check pattern is dict ??
        ## A1 ! check if all vars used in sprintf are declared
        ## check for quoted '%s' in sprintf text (not allowed).
        ## check that only all subs are %s and that the number of %s matches the length of the var list.
        ## re.search(r"\%(.)", , )  => from this get list to check all %s and length to check against var list.
        ## Given these checks - makes more sense to hardwire sprintf subfield names than use config approach.
        
        for field, field_content in self.pattern.items():
            if field not in self.pkey_dict:
                warnings.warn("Pattern has unknown field: %s !" % field)
        
        # The following is quite ugly and hard to follow.  Should probably be refactored
        oneOf = False
        oneOf_list = []
        for field, field_spec in self.pkey_dict.items():
            if field_spec['compulsory']:
                if field not in self.pattern:
                    warnings.warn("Pattern is missing compulsory field: %s !" % field)
            elif field_spec['OneOf']:
                oneOf_list.append(field)
                if field in self.pattern:
                    oneOf = True 
            if field_spec['sprintf']:
                if field in self.pattern:
                    for subfield in self.pattern[field]:
                        if subfield not in self.sprintf_keys:
                            warnings.warn("The field %s has an unknown subfield %s." % (field, subfield))
                    for subfield in self.sprintf_keys:
                        if subfield not in self.pattern[field]:
                            warnings.warn("The field %s lacks the compulsory subfield %s." % (field, subfield))
                    # Check that number of vars matches number %s in text field
                    if not len(re.findall('%s', self.pattern[field]['text'])) == len(self.pattern[field]['vars']):
                        warnings.warn("Wrong number of vars in field '%s' of %s" % (field, self.pattern['pattern_name']))
                    for v in self.pattern[field]['vars']:
                        if v not in self.pattern['vars']:
                            warnings.warn("%s not in varlist %s" % (v, str(self.pattern['vars'])))
# Move spec checks down:                            
#           if field_spec['msExpression']:
#               self._validate_quoted(field['text'])
#               self._validate_ms
                            
        if not oneOf:
            warnings.warn("Pattern must have at least one of: " + str(oneOf_list))

        # Poss to add: validate number of vars for sprintf subs
        
    def _validate_ms(self, sprintf):
        """ takes a sprintf ms field as input.  
        Subs quoted names for IDs.  
        Subs %s for Thing.  
        Runs SubClassOf query as a way of triggering exception if MS is bad."""
        #self.name2Id(sprintf)
        #re.sub("\'.+?\'", 'Thing', fu)
        #self.ont.getSubClasses('fu', 0)
        return
 
        

    def _validate_entities(self):
        """ Checks if IDs are known/non-obsolete. Warns and returns False if not.
        Otherwise returns True."""
        valid = True
        for NAME, ID in self.pattern['classes'].items():
            if not self.ont.knowsClass(ID):
                warnings.warn("Pattern contains unknown class %s ; %s." % (NAME, ID))
                valid = False
        for NAME, ID in self.pattern['relations'].items():
            if not self.ont.knowsObjectProperty(ID):
                warnings.warn("Pattern contains unknown relation %s, %s." % (NAME, ID))
                valid = False
        
        # TODO - add check for obsoletion status
        return valid
    
    def _validate_quoted(self, ms):
        # Check that everything quoted in an MS string is in dict:
        c = self.pattern['classes'].copy()
        lookup = c.update(self.pattern['relations'])
        out = True
        quoted = re.findall("\'(.+?)\'", ms)
        for q in quoted:
            if q not in lookup.keys():
                warnings.warn("Quoted element (%s) in MS string (%s) is not specified in pattern dictionary."  % (q, ms))
                out = False
        return out
                

    def _validate_range(self):
        # Boolean check for classes in range class expression - may require a different reasoner.
        return "Stub"
    

    def validate_abstract_pattern(self):
        """Validates pattern fields against spec and entities against ontology
        Returns True if both tests passed, otherwise returns False."""
        valid = True
        if not self._validate_pattern_fields():
            valid = False
        if not self._validate_entities():
            valid = False
        return valid


    def gen_name_id(self):
        """Returns a name:id dict for all entities in the pattern"""
        name_id  = {}
        name_id.update(self.pattern['classes'])
        name_id.update(self.pattern['relations'])
        return name_id
    
    def name2Id(self, classExpression):
        """Uses the list of entities in the pattern to sub all quoted entity names for IDs"""
        out = classExpression
        name_id = self.gen_name_id()
        for k, v in name_id.items():
            out = re.sub("\'"+k+"\'", v, out)  # Suspect this not Pythonic. Could probably be done with a fancy map lambda combo.  
        return out

    def _ms2md(self, msExpression):
        """Fully converts an msExpression to Markdown. Keywords -> italics; relations -> bold; entities -> hyperlinked."""
        msExpression = ms2Markdown.italic_keywords(msExpression)
        msExpression = ms2Markdown.bold_relations(msExpression, self.pattern['relations'].keys())
        name_id = self.gen_name_id()
        msExpression = ms2Markdown.hyperlink_quoted_entities(msExpression, name_id, self.baseURI)
        return msExpression
        
    def _var_quote_sub(self, text, VARS):
        """Quotes all members of list VARS with {}, then uses the resulting list in sprintf sub with target 'text'"""
        ## No need to live on class.  Can be moved to tools.  - Add assert test.
        qvars = map(lambda x: "\{ " + x + " \}", VARS)
        return text % tuple(qvars)
        

class abstract_pattern(metaPattern):
    """Class for validating and documenting (as md), design patterns."""
    def __init__(self, pattern, ont):
        self.pattern = pattern # pattern python data structure
        self.ont = ont
        self.validate_abstract_pattern()

    def __str__(self):
        return str(self.pattern)

    def _ms_sub_and_md(self, fieldName):
        """ Rolls a list of {} quoted vars for specified sprintf field."""
        l = []
        # for each var
        for v in self.pattern[fieldName]['vars']:
            l.append("{ " + v + " }") # roll a new list of vars, each deli
        ms_sub = self.pattern[fieldName]['text'] % tuple(l)
        return self._ms2md(ms_sub)

    def gen_markdown_doc(self):
        """Returns markdown documentation of abstract pattern"""
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
            out += "__equivalentTo:__ %s\n\n" % self._ms_sub_and_md('EquivalentTo')  # Ugly! Refactor!
        if "SubClassOf" in self.pattern:
            out += "__subClassOf:__ %s\n\n" % self._ms_sub_and_md('SubClassOf')
        if "GCI" in self.pattern:
            out += "__GCI:__ %s\n\n" % self._ms_sub_and_md('GCI')
        return out
        
    def update_entity_labels(self, ont):
        # This should report any changes, regenerate pattern.
        return "Stub"

        
class applied_pattern(metaPattern):
    """A pattern object with variable slots populated.
    Attributes with class expression values are named consistently with Manchester Syntax
    and use shortForm IDs.
    """

    def __init__(self, pattern, cdict, ont):
        """pattern = pattern python datastructure
        cdict = specification of vars as dict of 2 element tuples:
        { var1 : ( name , id ), var2: ( ... }
        ont = ontology = as Brain object """
        # Perhaps should be extended to allow specification of relations too?
        # Plus this dict of dict struc feels v.clunky to work with.  Either change or parse before using.
        self.pattern = pattern # pattern python data structure
        self.ont = ont
        self.validate_abstract_pattern()  # important to check that pattern is safe to apply.        
        self.cdict = cdict  # dict of name : id tuples
        
        # add entites from cdict to pattern dictionary
        for v in cdict.values():
            self.pattern["classes"][v[0]]=v[1]
        self.validate_applied_pattern()
        self.label = self._var_name_sub(self.pattern['name'])
        self.definition = self._var_name_sub(self.pattern['def'])
        
        # For each logical axioms type, add set to False if not present, otherwise sub var, then convert to IDs
        
        self.equivalentTo = False
        if "equivalentTo" in self.pattern:            
            self.equivalentTo = self.name2Id(self._var_id_sub(self.pattern['equivalentTo']))
        self.subClassOf = False
        if "subClassOf" in self.pattern:
            self.subClassOf = self.name2Id(self._var_id_sub(self.pattern['subClassOf']))
        self.GCI = False            
        if "GCI" in self.pattern:
            self.GCI = self.name2Id(self._var_id_sub(self.pattern['GCI']))
        
    def __str__(self):
        return str(self.pattern) + "\n\n" + str(self.cdict)
        
    def _var_id_sub(self, sprintf):  
        """sprintf =  a dict with text and vars keys, 
            vars = list for sprintf sub into text)
        Returns sprintf text vars substituted for ids, as specified 
        for applied pattern.
        """
        id_list = map(lambda x: self.cdict[x][1], sprintf["vars"] )
        return sprintf["text"] % tuple(id_list)
    
    def _var_name_sub(self, sprintf, quote=False):  
        """Takes a sprintf field as an arg and an optional boolean to specify quoting
        (a dict with text and vars keys, vars = list for sprintf sub into text)
        Returns sprintf text vars substituted for (optionally quoted) class names, as specified 
        for applied pattern.
        """
        q = ''
        if quote:
            q = "'"
        name_list = map(lambda x: q + self.cdict[x][0] + q, sprintf["vars"] )
        return sprintf["text"] % tuple(name_list)
    

    def gen_markdown_doc(self):
        # spec: follow Manchester syntax
        out = ''
        out += "__label:__ %s\n\n" % self._var_name_sub(self.pattern['name'])
        # sprintf to generate def - Use { var name } in sub
        out += "__def:__ %s\n\n" % self._var_name_sub(self.pattern['def'])
        
        if "equivalentTo" in self.pattern:            
            out += "__equivalentTo:__ %s\n\n" % self._ms2md(self._var_name_sub(self.pattern['equivalentTo'], True))
        if "subClassOf" in self.pattern:
            out += "__subClassOf:__ %s\n\n" % self._ms2md(self._var_name_sub(self.pattern['subClassOf'], True))
        if "GCI" in self.pattern:
            out += "__GCI:__ %s\n\n" % self._ms2md(self._var_name_sub(self.pattern['GCI'], True))
        return out

    def add_class_to_ont(self, ID):
        """Add a new class, with shortFormID = ID, following self.pattern, to self.ont"""
        self.ont.addClass(ID)
        self.ont.label(ID, self.label)
        self.ont.annotation(ID, 'IAO_0000115', self.definition)
        if 'equivalentTo' in self.pattern:
            self.ont.equivalentClasses(ID, self.equivalentTo)
        if 'subClassOf' in self.pattern:
            self.ont.subClassOf(ID, self.subClassOf)
        # Don't currently have means to generate GCIs!

        
    def validate_applied_pattern(self):
        self._validate_var_entities()
        #self._has_subclasses()  # only needed for reporting purposes.

    def _validate_var_entities(self):
        for v in self.pattern['vars']:
            if v not in self.cdict:
                warnings.warn("Pattern %s required var %s to be specified. It is not." % (self.pattern['name'], v))
        for v, c in self.cdict.items():
            if v not in self.pattern['vars']:
                warnings.warn("Pattern %s does not include specified var %s." % (self.pattern['name'], v))
            else:
                if not self.ont.knowsClass(c[1]):
                    warnings.warn("Unknown class, %s, specified for var %s" % (c[0], v))

                
    def _has_subclasses(self, ont):
        return "Stub"
        # Boolean check for the presence of inferred subclasses.
        


        

        
