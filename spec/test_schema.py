import yaml
from jsonschema import Draft4Validator
import sys

dosdp_core_file = open("DOSDP_schema_core.yaml", "r")
dosdp_core = yaml.load(dosdp_core_file.read())

v = Draft4Validator(dosdp_core)


test_positive_file = open("test/test_positive.yaml", "r")
test_positive = yaml.load(test_positive_file.read())

if not v.is_valid(test_positive):
    es = v.iter_errors(test_positive)
    for e in es: 
        print(e)
    sys.exit(1)
    
else:
    print(True)
