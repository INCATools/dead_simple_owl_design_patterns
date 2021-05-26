import unittest
import os
from dosdp.document.schema import schema_create_docs
from dosdp.document.pattern import patterns_create_docs as pattern_doc
from dosdp.document import document


class DocumentGenerationCase(unittest.TestCase):

    def tearDown(self):
        """
        Delete files generated during tests
        """
        if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../generic_test/acute.md")):
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../generic_test/acute.md"))

        if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       "../positive_test_set/patterns/data/acute.md")):
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "../positive_test_set/patterns/data/acute.md"))

        if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       "../positive_test_set/patterns/data/generated/acute.md")):
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "../positive_test_set/patterns/data/generated/acute.md"))

        if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       "../positive_test_set/patterns/data/generated/acute2.md")):
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "../positive_test_set/patterns/data/generated/acute2.md"))

        if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       "../positive_test_set/patterns/data/generated/overview.md")):
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "../positive_test_set/patterns/data/generated/overview.md"))

        if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       "./dosdp_schema2.md")):
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "./dosdp_schema2.md"))

        if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       "../positive_test_set/patterns/data/generated/schema.md")):
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "../positive_test_set/patterns/data/generated/schema.md"))

    def test_mapping_definition_search(self):
        mappings = schema_create_docs.find_mapping_definitions()

        for key in mappings.keys():
            print(key + " -->" + mappings[key])

        self.assertTrue("printf_annotation_obo$xrefs" in mappings.keys())
        self.assertEqual("oboInOwl:hasDbXref", mappings["printf_annotation_obo$xrefs"])

        self.assertTrue("name" in mappings.keys())
        self.assertEqual("rdfs:label", mappings["name"])

        self.assertTrue("generated_narrow_synonyms$items" in mappings.keys())
        self.assertEqual("oboInOwl:hasNarrowSynonym", mappings["generated_narrow_synonyms$items"])

        self.assertTrue("generated_synonyms$items" in mappings.keys())
        self.assertEqual("oboInOwl:hasExactSynonym", mappings["generated_synonyms$items"])

    def test_is_schema(self):
        self.assertTrue(pattern_doc.is_dosdp_pattern_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                    "../positive_test_set/patterns/anchored_membrane_component.yaml")))
        self.assertFalse(pattern_doc.is_dosdp_pattern_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                     "../../dosdp_schema2.yaml")))
        self.assertFalse(pattern_doc.is_dosdp_pattern_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                     "../../dosdp_schema.yaml")))
        self.assertTrue(pattern_doc.is_dosdp_pattern_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                    "../positive_test_set/patterns/expression_pattern.yaml")))
        self.assertFalse(pattern_doc.is_dosdp_pattern_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                     "../negative_test_set/dummy.yaml")))

    def test_pattern_interface_single_param(self):
        document.generate_pattern_documentation(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                             "../positive_test_set/patterns/data/acute.yaml"))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                    "../generic_test/acute.md")))

    def test_pattern_interface_two_param(self):
        document.generate_pattern_documentation(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                             "../positive_test_set/patterns/data/acute.yaml"),
                                                os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                             "../positive_test_set/patterns/data/acute.md"))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                    "../positive_test_set/patterns/data/acute.md")))

        self.assertFalse(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                     "../positive_test_set/patterns/data/overview.md")))

    def test_pattern_interface_folder_input(self):
        document.generate_pattern_documentation(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                             "../positive_test_set/patterns/data/"),
                                                os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                             "../positive_test_set/patterns/data/generated"))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                    "../positive_test_set/patterns/data/generated/acute.md")))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                    "../positive_test_set/patterns/data/generated/acute2.md")))
        self.assertFalse(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                     "../positive_test_set/patterns/data/generated/dummy.md")))

    def test_pattern_interface_non_pattern(self):
        document.generate_pattern_documentation(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                             "../positive_test_set/patterns/data/dummy.yaml"))
        self.assertFalse(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                     "../generic_test/dummy.md")))

    def test_pattern_interface_folder_none_params(self):
        document.generate_pattern_documentation(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                             "../positive_test_set/patterns/data/"))
        self.assertFalse(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                     "../positive_test_set/patterns/data/generated/acute.md")))

    def test_patterns_interface_overview(self):
        document.generate_pattern_documentation(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                             "../positive_test_set/patterns/data/"),
                                                os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                             "../positive_test_set/patterns/data/generated"))

        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                    "../positive_test_set/patterns/data/generated/overview.md")))

    def test_schema_interface(self):
        document.generate_schema_documentation()
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                    "./dosdp_schema2.md")))

    def test_schema_interface_single_param(self):
        document.generate_schema_documentation(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                            "../positive_test_set/patterns/data/generated/schema.md"))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                    "../positive_test_set/patterns/data/generated/schema.md")))


if __name__ == '__main__':
    unittest.main()
