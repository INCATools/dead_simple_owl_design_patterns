import re
#from uk.ac.ebi.brain.core import Brain
#from OBO_ID_gen import ontId # Avoid dependency on this ?

from abc import ABCMeta, abstractmethod

class X:
    # A class for storing a specific input var spec
    def __init__(self, x_instance, x_range):
        self.instance = x_instance
        self.range = x_range
    def validate_X(self, ont):
        # Takes brain object as an import. Checks that instance is subclassOf specified range. # But Brain obviously not good for unions...
        ont.subClassOf(self.x_range, self.x_instance)

class pattern:
    __metaclass__ = ABCMeta     # Abstract class - should not be directly instantiated

    # Define interface here????

    # Subclass validation?
    
    @abstractmethod
    def gen_ivar(self, l):
        return l[0] % tuple(map(lambda x: x.instance, l[1:]))

    def gen_cvar(self, l):
        return l[0] % tuple(map(lambda x: x.range, l[1:]))
        
    def validate_pattern(self, ont):
        x = 1 # stub
        # validate individual entities
        # Need classes and relations to be kept separately for this to work with Brain
        
        # validate class expression
        # Does it have subclasses
        
        # Validate target range
        # Does it parse?
        # Does it have subclasses

    def classExp_label2Id(self):
        # Assumes all labels are quoted, converts these to IDs by regex using dict
        return re.sub("'(.+?)'", (lambda m: self.owl_entities[m.group(1)]), self.ex_pattern) #  If 2nd arg (repl) is a function, it automatically takes the match object as arg.
        
    def __str__(self):
        return "label: %s\ndef: %s\nEquivalentTo: %s" % (self.gen_ivar(self.name_pattern), self.gen_ivar(self.def_pattern), self.gen_ivar(self.ex_pattern))
    
    def pattern_doc(self):
        return "label: %s\ndef: %s\nEquivalentTo: %s" % (self.gen_cvar(self.name_pattern), self.gen_cvar(self.def_pattern), gen_cvar(self.ex_pattern))
            
    def generate_class(self, ont, sfid):
            # ont = a brain object, sfid = short form ID.
            ont.addClass(sfid)
            ont.label(sfid, gen_ivar(self.name_pattern))
            ont.annotation(sfid, 'http://www.geneontology.org/formats/oboInOwl#hasOBONamespace', self.namespace)
            ont.equivalentClass(sfid, classExp_label2Id(gen_ivar(self.ex_pattern))) # Should really clean this up!
        

class X_import_into_cell(pattern):
    owl_entities = { 'transport' : 'GO_0006810', 'extracellular region': 'GO_0005576', 'intracellular part' : 'GO_0044424' } # Class var, not instance var.
    owl_relations = { 'has target start location' : 'RO_0002338', 'has target end location' : 'RO_0002339', 'imports': 'RO_0002340'  }
    x_range = ("'chemical entity' OR 'protein' OR 'protein complex'")
    def __init__(self, imported):
        self.imported = X(imported, x_range)
        self.ex_pattern =  ("'transport' " \
            "and ('has target start location' some 'extracellular region') " \
            "and ('has target end location' some 'intracellular part') " \
            "and ('imports' some '%s')", self.imported)
        self.def_pattern = ("The directed movement of %s from outside of a cell into the cytoplasmic compartment. This may occur via transport across the plasma membrane or via endocytosis.", self.imported)
        self.name_pattern = ("%s import into cell", self.imported)
        
class X_import_across_plasma_membrane(X_import_into_cell):
    X_import.owl_classes.update( { 'plasma membane' : '', 'cytosol' : '' } )  # For simplicity, it may be better to give up inheritance, except to pattern
    X_import.owl_relations.update( { 'results_in_transport_across': '' } )
    def __init__(self, imported):
        self.imported = (imported, X_import_to_cell.x_range) # check
        self.equivalentTo = "'transport' " \
        "and ('has target start location' some 'extracellular region') " \
        "and ('has target end location' some 'cytosol') " \
        "and ('imports' some %s) " \
        "and ('results_in_transport_across' some 'plasma membane'" % self.imported
        
        self.definition = "The directed movement of %s from outside of a cell, across the plasma membrane and into the cytosol." % self.imports
        
        self.name = "%s import across plasma membrane" % self.imports


