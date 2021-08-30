import unittest
import os
import pathlib
from ruamel.yaml import YAML, YAMLError
from jsonschema import Draft4Validator

SCHEMA = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                      "../../dosdp_schema.yaml")
POSITIVE_PATTERN_1 = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "../positive_test_set/patterns/acute.yaml")
POSITIVE_PATTERN_2 = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "../positive_test_set/patterns/multi_clause_schema.yaml")
NEGATIVE_PATTERN_1 = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "../negative_test_set/acute_negative.yaml")


def show_errors(pattern, validator):
    es = validator.iter_errors(pattern)
    for e in es:
        print(" => ".join([str(e.schema_path), str(e.message), str(e.context)]))


class SchemaValidationTests(unittest.TestCase):

    def test_schema_validity1(self):
        self.assertTrue(pathlib.Path(SCHEMA).exists())

        validator = Draft4Validator(self.read_yaml(SCHEMA))

        ## self.show_errors(pattern, validator)
        self.assertTrue(validator.is_valid(self.read_yaml(POSITIVE_PATTERN_1)))
        self.assertTrue(validator.is_valid(self.read_yaml(POSITIVE_PATTERN_2)))

        negative_pattern_1 = self.read_yaml(NEGATIVE_PATTERN_1)
        self.assertFalse(validator.is_valid(negative_pattern_1))
        es = validator.iter_errors(negative_pattern_1)

        # failing because def does not have a text
        self.assertEqual("{'vars': ['disease']} is not valid under any of the given schemas", next(es).message)

    def read_yaml(self, yaml_path):
        with open(yaml_path, "r") as stream:
            try:
                yaml_file = YAML(typ='safe').load(stream)
            except YAMLError as exc:
                self.fail("Yaml read failed:"+yaml_path)
        return yaml_file

