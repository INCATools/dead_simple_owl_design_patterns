import unittest
from dosdp import document


class DocumentGenerationCase(unittest.TestCase):

    def test_mapping_definition_search(self):
        mappings = document.find_mapping_definitions()

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


if __name__ == '__main__':
    unittest.main()
