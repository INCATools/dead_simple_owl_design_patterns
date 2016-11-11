import yaml
import json
from jsonschema import Draft4Validator

dosdp_core_file = open("DOSDP_schema_core.yaml", "w")
dosdp_core = yaml.load(dosdp_core_file)

v = Draft4Validator(dosdp_core)


test_positive_file = open("test/postive_test.yaml", "w")
test_positive = yaml.load(test_positive_file)

if not v.is_valid(test_positive):
    es = v.iter_errors(test_positive)
    for e in es: print(e)
else:
    print(True)
