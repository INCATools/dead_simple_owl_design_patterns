#!/usr/bin/env Jython -Xmx4000m
from pattern import applied_pattern
from pattern import load_json_from_file
import sys
sys.path.append("../src")
from brain_io_wrapper import load_brain_from_file, save_brain_as_ofn
from ID_tools import goId
# TBA - import ID generation script

"""This example script assumes the user is editing a local GO file (Arg 3), saving to the same file.
Arg 1 = a pattern file
Arg 2 = specification of vars
Arg 3 = A *full* path to the GO OWL file to be edited.
"""

### Load up a brain with GO
go = load_brain_from_file(sys.argv[3])
goid = goId(go = go, start = 9000000, end = 9000100)
pattern = load_json_from_file(path = sys.argv[1])
var_spec = load_json_from_file(path = sys.argv[2])

for spec in var_spec:
    ap = applied_pattern(pattern = pattern, cdict = spec, ont = go)
    ID = goid.gen_id(name = ap.label)  # Call to ID generation thingy.
    ap.add_class_to_ont(ID)

# Move save out of Brain.
save_brain_as_ofn(brain = go, path = "file://" + sys.argv[3]) # No brain method to choose syntax
go.sleep()

