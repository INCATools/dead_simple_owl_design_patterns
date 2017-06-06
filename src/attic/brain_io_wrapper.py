#!/usr/bin/env Jython -Xmx4000m

from uk.ac.ebi.brain.core import Brain
from org.semanticweb.owlapi.io import OWLFunctionalSyntaxOntologyFormat
from org.semanticweb.owlapi.model import IRI
from java.io import File
from org.semanticweb.owlapi.apibinding.OWLManager import createOWLOntologyManager

# Kinda sucks that this is needed. Should be written into some extension to Brain.

def load_brain_from_file(path):
    """Created a Brain object from a file, preserving ontology metadata.
    path = path to file.  May be absolute or relative.
    """
    m = createOWLOntologyManager()
    o_file = File(path)
    o = m.loadOntologyFromOntologyDocument(o_file)
    return Brain(o)

def save_brain_as_ofn(brain, path):
    """
    Wot it sez on' tin.
    brain = Brain object
    path = *FULL* path to file (relative paths not allowed).
    """
    ofn = OWLFunctionalSyntaxOntologyFormat()
    brain.manager.saveOntology(brain.getOntology(), ofn, IRI.create("file://" + path))
