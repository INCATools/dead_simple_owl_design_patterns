#!/usr/bin/env jython -J-Xmx8000m

import json
import pattern
import glob
import re
from uk.ac.ebi.brain.core import Brain
import sys


"""Runs verification tests on abstract patterns and generates markdown docs.
1st ARG specifies path to input/output files.  
Second ARG specifies ontology file to use in validation."""

def load_json_from_file(path):
    json_file = open(path, "r")
    json_string = json_file.read()
    json_file.close()
    return json.loads(json_string)

# Testing abstract pattern validation and documentation
o = Brain()
o.learn(sys.argv[2]) # Running with local file for now.
# Switch this to specify path as argv
json_files = glob.glob(sys.argv[1] + "*.json")  # Note - glob returns full file path

for f in json_files:
    p = load_json_from_file(f)
    m = re.search("(.+).json", f)
    pattern_name = m.group(1)
    print "Processing %s" % pattern_name
    ap = pattern.abstract_pattern(p, o)
    md = open(pattern_name + ".md", "w")
    #print ap.gen_markdown_doc()
    md.write(ap.gen_markdown_doc())
    md.close()
    o.sleep()
