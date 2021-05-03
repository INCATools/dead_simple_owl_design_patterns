import unittest
import os


from dosdp.validator import validate

POSITIVE_PATTERNS_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../positive_test_set/patterns")
POSITIVE_PATTERN_1 = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "../positive_test_set/export_across_membrane.yaml")

NEGATIVE_PATTERN_INDENTATION = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                            "../negative_test_set/wrong_indentation.yaml")
NEGATIVE_PATTERN_QUOTES = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       "../negative_test_set/quotes_miss_match.yaml")
NEGATIVE_PATTERN_UNDECLARED_VAR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                               "../negative_test_set/undeclared_var.yaml")
NEGATIVE_PATTERN_UNDECLARED_CLASS = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                 "../negative_test_set/undeclared_class.yaml")
NEGATIVE_PATTERN_UNDECLARED_REL = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                               "../negative_test_set/undeclared_relation.yaml")


class ValidatorTest(unittest.TestCase):

    def test_positive_folder(self):
        self.assertTrue(validate(POSITIVE_PATTERNS_FOLDER))

    def test_positive_file(self):
        self.assertTrue(validate(POSITIVE_PATTERN_1))

    def test_wrong_indentation(self):
        self.assertFalse(validate(NEGATIVE_PATTERN_INDENTATION))

    def test_undeclared_var(self):
        self.assertFalse(validate(NEGATIVE_PATTERN_UNDECLARED_VAR))

    def test_undeclared_class(self):
        self.assertFalse(validate(NEGATIVE_PATTERN_UNDECLARED_CLASS))

    def test_undeclared_relation(self):
        self.assertFalse(validate(NEGATIVE_PATTERN_UNDECLARED_REL))

