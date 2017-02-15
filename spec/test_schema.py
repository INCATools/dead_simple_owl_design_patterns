import yaml
from jsonschema import Draft4Validator
import warnings

dosdp_full_file = open("DOSDP_schema_full.yaml", "r")
dosdp = yaml.load(dosdp_full_file.read())

def test_jschema(validator, file_path):
    test_file = open(file_path, "r")
    test_pattern = yaml.load(test_file.read())

    if not validator.is_valid(test_pattern):
        es = validator.iter_errors(test_pattern)
        for e in es:
            warnings.warn(str(e))
            return False
    else:
        return True

V = Draft4Validator(dosdp)
stat = True

# Test core - positive
if not test_jschema(V, "test/test_positive.yaml"): stat = False
# Test obo - positive
if not test_jschema(V, "../patterns/import_across_membrane.yaml"): stat = False

if not stat:
    sys.exit(1)



# TODO - add some negative tests - designed to fail to test aspects of spec.

