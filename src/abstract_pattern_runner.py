import json
import pattern
import glob
import re
from uk.ac.ebi.brain.core import Brain


"""Project specific runner script. Runs verification tests on abstract patterns and generates markdown docs"""

def load_json_from_file(path):
    json_file = open(path, "r")
    json_string = json_file.read()
    json_file.close()
    return json.loads(json_string)

# Testing abstract pattern validation and documentation
o = Brain()
#o.learn("file:///repos/go_trunk_ont/extensions/go-plus.owl") # Running with local file for now.

json_files = glob.glob("../patterns/*.json")  # Note - glob returns full file path

for f in json_files:
    p = load_json_from_file(f)
    m = re.search("(.+).json", f)
    pattern_name = m.group(1)
    ap = pattern.abstract_pattern(p, o)
    md = open(pattern_name + ".md", "w")
    print ap.gen_markdown_doc()
    md.write(ap.gen_markdown_doc())
    md.close()
    o.sleep()
