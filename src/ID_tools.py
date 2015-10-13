#!/usr/bin/env jython
import warnings
import uuid

class ontId:
    """Generate an OBOish OWL shortform ID given specifications of idp, accession length and an id_name dict."""
    def __str__(self):
        return "IDP: %s; accession length: %d; Separator: '%s'; number of IDs in dict: %d" % (self.idp, self.length, self.sep, len(self.id_name.keys()))
    def __init__(self, idp, length, id_name):
        """ARG1: ID prefix (string), ARG2, length of numeric portion ID, ARG3 an id:name hash"""
        # if type(length) not integer  # How to properly add type checks here?
        # if type(id_name) not dict  # How to properly add type checks here?
        self.idp = idp
        self.length = length
        self.id_name = id_name
        self.sep = '_'
        self.accession = 1 # default starting accession for init.
        self.name_id = dict((v,k) for k, v in id_name.iteritems())
    def gen_id(self, name):
        return self._gen_id(name)
    def _gen_id(self, name):
        k = self._gen_key ()
        while k in self.id_name:
            self.accession += 1
            k = self._gen_key()
        self.id_name[k]=name
        self.name_id[name] = k
        return k #
    def _gen_key(self):
        dl = len(str(self.accession)) # coerce int to string.
        k = self.idp+self.sep+(self.length - dl)*'0'+str(self.accession)
        return k
    
class ontId_owl(ontId):
    def __init__(self, idp, length, ont, start, end):
            """Generate an OBOish OWL shortform ID given specifications of: 
            idp; accession length; Brain object and the start & end of an ID range.
            Assumes all existing IDs are used for *classes* in Ontology."""
            self.ont = ont
            self._gen_lookups()
            self.accession = start
            self.end = end
            self.length = length

    def _gen_lookups(self):
        self.id_name = {}
        self.name_id = {}
        clist = self.ont.getSubClasses("Thing", 0)
        for c in clist:
            n = uuid.uuid4()
            try:
                n = self.ont.getLabel(c) # Isolating this lookup in case names missing! Maybe better to not bother making lookup.
            except:
                pass
            self.id_name[c]=n
            self.name_id[n]=c
    
    def gen_id(self, name):
        newid = self._gen_id(name)
        if self.accession > self.end:
            warnings.warn("Generated ID is past end of range!") # Should raise an exception here!
            return False 
        else:
            return newid

    
class goId(ontId_owl):
    """An object for generating GO id, given 
    go: a Brain object, loaded with GO.
    start: start of range (int)
    end: end of range (int)
    """
    def __init__(self, go, start, end):
        self.idp = 'GO'
        self.length = 7
        self.sep = '_'
        self.ont = go
        self._gen_lookups()
        self.accession = start
        self.end = end
        

    
    




def test_gen_id():
    # make a dict

    id_name = {}
    id_name['HSNT:00000001'] = 'head'
    id_name['HSNT:00000002'] = 'shoulders'
    id_name['HSNT:00000003']= 'knees'

    hsnt = ontId('HSNT', 8, id_name)
    hsnt.sep = ':'

    # Generate ID for new term 'toes'
    k = hsnt.gen_id('toes')
    # Change these to warnings:
    if (k == 'HSNT:00000004') & (hsnt.id_name[k] == 'toes'):
        return True
    else: 
        warnings.warn('gen_id is broken')
        return False


test_gen_id()
