import warnings
import yaml
import json


# Two major requirements:
## testing of patterns
## testing of instances
# Should these be split, or carried out by the same object?

# Pattern for turning a list, l in which the first arg is a sprintf statement and all subsequent args are the substitutions on that sprintf statement.
# def sprintf_sub(self, l):
#     return l[0] % tuple(map(lambda x: x.label, l[1:]))


class pattern:
    # class level vars
    self.pkey_dict = { "pattern_name" : { "compulsory" = True, "sprintf" = False } "classes" : { "compulsory" = True, "sprintf" = False } , "relations" : { "compulsory" = True, "sprintf" = False }, "vars" :  { "compulsory" = True, "sprintf" = False }, "name" : { "compulsory" = True, "sprintf" = True }, "def" : { "compulsory" = True, "sprintf" = True }, "EquivalentTo" : { "compulsory" = False, "OneOf = True, sprintf" = True }, "SubclassOf" : { "compulsory" = False, "OneOf = True, sprintf" = True }, "GCI" : { "compulsory" = False, "OneOf = False, sprintf" = True } }  # Better to specify this in JSON OR YAML in first place.
    
    self.sprintf_keys = ("text", "vars")  # Perhaps embed this in pkey_dict.  Gives more scope for clearer names for fields. OTOH, code will be simpler with generic names.
    
    def __init__(self, pattern, clist, ont):
       self.pattern = yaml.load(pattern) # better to use json and convert from yaml first?
       self.clist = clist  # Must be a list of name : ID tuples?  Might be nice if this could be yaml/json too.
       self.validate(ont)

    def __string__(self):
        # Return string should include subs. Perhaps just make into 
        stub = 1

    def 

    def gen_markdown(self):
        stub = 1

    def _sprintf_vsub
        
    def validate(self, ont):
        _validate_pattern_fields()
        _validate_entities(ont)
        _validate_range(ont)
        _has_subclasses(ont)

    def validate_pattern_fields(self):
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
                        if key2 not in 

            
                
                
                

        if key not in self.pattern.keys():

              
        # validate dict sub keys
        # validate number of vars for sprintf subs

    def _validate_entities(self, ont):
        # Check IDs are valid
        for c in self.pattern['classes']:
            if not ont.knowsClass(c):
                warnings.warn("Pattern contains unknown class %s" % c)
        for o in self.pattern['relations']:
            if not ont.knowsObjectProperty(o):
                warnings.warn("Pattern contains unknown relation")
                

    def _update_entity_labels(ont):
        # This should report any changes, regenerate pattern.
        stub = 1

    def _validate_range(self, ont):
        # Boolean check for classes in range class expression
        stub = 1

    def _has_subclasses(self, ont):
        # Boolean check for the presence of inferred subclasses.
        stub = 1


        
       
