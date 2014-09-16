#!/usr/bin/env python

import json_yaml_tools
import glob
import re

# FInd all YAML files in directory.
yaml_files = glob.glob("../patterns/*.yaml")  # Not - glob returns full file path

for f in yaml_files:
    m = re.search("(.+).yaml", f)
    pattern_name = m.group(1)
    json_yaml_tools.yaml2json(f, pattern_name + ".json")
    
     

# Run conversion to JSON