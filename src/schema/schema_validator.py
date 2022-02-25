import os
from ruamel.yaml import YAML
from jsonschema import Draft7Validator

SCHEMA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../schema/dosdp_schema.yaml")


ryaml = YAML(typ='safe')
with open(SCHEMA_PATH) as stream:
    dosdp_schema = ryaml.load(stream)

Draft7Validator.check_schema(dosdp_schema)
