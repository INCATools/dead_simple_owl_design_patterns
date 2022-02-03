import logging
import os
import ruamel.yaml
from dosdp.normalise.base_normaliser import BaseNormaliser
from dosdp.normalise.util import read_yaml_file

logging.basicConfig(level=logging.INFO)


class ElementOrderNormaliser(BaseNormaliser):
    """
    Order of the pattern elements should be same with the element order in the schema.
    """

    SCHEMA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../schema/dosdp_schema.yaml")

    def normalise(self, pattern):
        logging.info("Normalising elements' order.")
        schema = read_yaml_file(self.SCHEMA_PATH)
        schema_properties = schema["properties"]
        schema_definitions = schema["definitions"]

        sorted_map = ruamel.yaml.comments.CommentedMap()
        elements = list(pattern.keys())
        sorted_elements = sorted(elements, key=list(schema_properties.keys()).index)

        order = 0
        for element_name in sorted_elements:
            print(element_name)
            if "$ref" in schema_properties[element_name]:
                # handle Map
                print("$ref: " + str(type(pattern[element_name])))
                definition_name = str(schema_properties[element_name]["$ref"]).replace("#/definitions/", "")
                sorted_element = self.sort_element_based_on_definition(pattern[element_name],
                                                                       schema_definitions, definition_name)
                sorted_map.insert(order, element_name, sorted_element)
            elif "items" in schema_properties[element_name] and "$ref" in schema_properties[element_name]["items"]:
                # handle list
                print("list $ref: " + str(type(pattern[element_name])))
                sub_element_list = ruamel.yaml.comments.CommentedSeq()
                definition_name = str(schema_properties[element_name]["items"]["$ref"]).replace("#/definitions/", "")
                for element in pattern[element_name]:
                    sub_element_list.append(self.sort_element_based_on_definition(element,
                                                                                  schema_definitions, definition_name))
                sorted_map.insert(order, element_name, sub_element_list)
            else:
                # handle simple data structure
                print(type(pattern[element_name]))
                sorted_map.insert(order, element_name, pattern[element_name])
            order += 1

        return sorted_map

    def sort_element_based_on_definition(self, element, schema_definitions, definition_name):
        """
        Creates a new sorted CommentedMap based on the property ordering in the schema_definition.
        """
        sorted_element = ruamel.yaml.comments.CommentedMap()

        if "properties" in schema_definitions[definition_name]:
            expected_order = list(schema_definitions[definition_name]["properties"].keys())
        elif "oneOf" in schema_definitions[definition_name]:
            expected_order = list()
            for option in schema_definitions[definition_name]["oneOf"]:
                option_def_name = str(option["$ref"]).replace("#/definitions/", "")
                option_order = list(schema_definitions[option_def_name]["properties"].keys())
                insert_index = len(expected_order)
                for prop in reversed(option_order):
                    if prop not in expected_order:
                        expected_order.insert(insert_index, prop)
                    else:
                        insert_index = expected_order.index(prop)
        sorted_property_names = sorted(list(element.keys()), key=expected_order.index)
        order = 0
        for property_name in sorted_property_names:
            sorted_element.insert(order, property_name, element[property_name])
            order += 1
        return sorted_element
