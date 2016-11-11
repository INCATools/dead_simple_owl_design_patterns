import yaml
import json
from jsonschema import Draft4Validator

test_positive_file = open("test/postive_test.yaml", "w")

test_positive = yaml.loads(test_positive_file)


v = Draft4Validator(dosdp_core)
if not v.is_valid(test_positive):
    es = v.iter_errors(test_positive)
    for e in es: print(e)
else:
    print(True)
