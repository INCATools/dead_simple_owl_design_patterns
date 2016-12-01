#!/usr/bin/env python

import json_yaml_tools
import glob
import re
import sys

"""Convert all yaml files in a specified directory (arg1) into json files
"""

# FInd all YAML files in directory.
yaml_files = glob.glob(sys.argv[1] + "*.yaml")  # Note - glob returns full file path

for f in yaml_files:
    m = re.search("(.+).yaml", f)
    pattern_name = m.group(1)
    json_yaml_tools.yaml2json(f, pattern_name + ".json")
    
     

# Run conversion to JSON
