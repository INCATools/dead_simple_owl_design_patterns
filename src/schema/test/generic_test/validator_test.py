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
NEGATIVE_PATTERN_UNDECLARED_REL_MC = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                  "../negative_test_set/undeclared_relation_multi_clause.yaml")
NEGATIVE_PATTERN_AXIOM_CLAUSE_NESTING = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                     "../negative_test_set/axiom_multi_clause_nesting.yaml")
NEGATIVE_PATTERN_AXIOM_SEPARATOR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                "../negative_test_set/axiom_separator.yaml")
NEGATIVE_PATTERN_MULTI_CLAUSE_MULTI_LIST = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                        "../negative_test_set/multi_clause_with_multi_list.yaml")
NEGATIVE_PATTERN_MULTI_CLAUSE_MULTI_LIST2 = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                         "../negative_test_set/multi_clause_with_multi_list2.yaml")
NEGATIVE_PATTERN_UNDECLARED_ANNOT_PROP = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                      "../negative_test_set/undeclared_annotation_prop.yaml")
NEGATIVE_PATTERN_SCHEMA = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       "../negative_test_set/not_schema_compliant.yaml")


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
        self.assertFalse(validate(NEGATIVE_PATTERN_UNDECLARED_REL_MC))

    def test_axiom_clause_nesting(self):
        self.assertFalse(validate(NEGATIVE_PATTERN_AXIOM_CLAUSE_NESTING))

    def test_axiom_separator(self):
        self.assertFalse(validate(NEGATIVE_PATTERN_AXIOM_SEPARATOR))

    def test_single_list_per_multi_clause(self):
        self.assertFalse(validate(NEGATIVE_PATTERN_MULTI_CLAUSE_MULTI_LIST))
        self.assertFalse(validate(NEGATIVE_PATTERN_MULTI_CLAUSE_MULTI_LIST2))

    def test_undeclared_annotation_prop(self):
        self.assertFalse(validate(NEGATIVE_PATTERN_UNDECLARED_ANNOT_PROP))

    def test_schema_validation(self):
        self.assertFalse(validate(NEGATIVE_PATTERN_SCHEMA))
