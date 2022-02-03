import unittest
import os
from pathlib import Path


from dosdp.normalise import normalizer

WRONG_ORDER_1 = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "../normalisation_test_set/wrong_order1.yaml")
WRONG_INDENT = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "../normalisation_test_set/wrong_indentation.yaml")
WRONG_SPACING = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "../normalisation_test_set/wrong_spacing.yaml")
NORMALISED_OUTPUT = Path(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                      "../normalisation_test_set/normalised_output.yaml"))
COMMENTS_ORDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              "../normalisation_test_set/comments_ordering.yaml")


class NormalizerTest(unittest.TestCase):

    # def tearDown(self):
    def setUp(self):
        """
        Delete files generated during tests
        """
        if os.path.exists(NORMALISED_OUTPUT):
            os.remove(NORMALISED_OUTPUT)

    def test_order_normalisation(self):
        normalizer.normalise(WRONG_ORDER_1, NORMALISED_OUTPUT)
        print(NORMALISED_OUTPUT)
        output = normalizer.read_yaml_file(NORMALISED_OUTPUT)
        expected_order = ["pattern_name", "pattern_iri", "contributors", "description", "classes", "relations",
                          "annotationProperties", "vars", "annotations", "equivalentTo", "name", "def"]

        self.assertEqual(list(output.keys()), expected_order)

    # def test_comment_order_normalisation(self):
    #     normalizer.normalise(COMMENTS_ORDER, NORMALISED_OUTPUT)
    #     print(NORMALISED_OUTPUT)
    #     output = normalizer.read_yaml_file(NORMALISED_OUTPUT)

    def test_sub_element_order_normalisation(self):
        normalizer.normalise(WRONG_ORDER_1, NORMALISED_OUTPUT)
        print(NORMALISED_OUTPUT)
        output = normalizer.read_yaml_file(NORMALISED_OUTPUT)

        self.assertEqual(list(output["equivalentTo"].keys()), ["text", "vars"])
        self.assertEqual(list(output["name"].keys()), ["text", "vars"])
        self.assertEqual(list(output["annotations"][0].keys()), ["annotationProperty", "text", "vars"])

        # do not edit classes
        self.assertEqual(list(output["classes"].keys()), ["acute", "disease"])

    def test_indentation_normalisation(self):
        normalizer.normalise(WRONG_INDENT, NORMALISED_OUTPUT)
        output = open(NORMALISED_OUTPUT, 'r')
        lines = output.readlines()

        previous_indentation = 0
        line_number = 1
        for line in lines:
            if line.strip():
                leading_spaces = len(line) - len(line.lstrip())
                if not (leading_spaces == 0 or
                        leading_spaces == previous_indentation or
                        leading_spaces == previous_indentation + 2 or
                        leading_spaces == previous_indentation - 2):
                    print("leading spaces: " + str(leading_spaces))
                    print("previous indent: " + str(previous_indentation))
                    self.fail("Wrong indentation at line: " + str(line_number) + " '" + line + "'")
                previous_indentation = leading_spaces
            else:
                # empty line
                previous_indentation = 0
            line_number += 1

        output.close()

    def test_spacing_normalisation(self):
        normalizer.normalise(WRONG_SPACING, NORMALISED_OUTPUT)
        output = open(NORMALISED_OUTPUT, 'r')
        lines = output.readlines()

        previous_line = "\n"
        line_number = 1
        for line in lines:
            if line.strip():
                leading_spaces = len(line) - len(line.lstrip())
                if leading_spaces == 0 and not line.startswith("- "):
                    # there should be an empty line before every top level element
                    print(line)
                    self.assertEqual(previous_line, "\n")
            elif not previous_line.strip():
                self.fail("Consecutive empty lines at line: " + str(line_number) + " '" + line + "'")
            previous_line = line
            line_number += 1

        output.close()
