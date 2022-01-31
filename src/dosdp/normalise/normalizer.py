import logging
import os
import ruamel.yaml
from ruamel.yaml import YAML, YAMLError
from ruamel.yaml.tokens import CommentToken
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)


class BaseNormaliser(ABC):

    @abstractmethod
    def normalise(self, pattern):
        pass


class NewLineNormaliser(BaseNormaliser):
    """
    There should be a single empty line between elements.
    """

    def normalise(self, pattern):
        logging.info("Normalising spacing between elements.")
        print(len(pattern))
        print(type(pattern))
        print(pattern.ca)
        print(type(pattern.ca.items))
        print(list(pattern.ca.items.keys()))

        self.remove_top_level_newlines(pattern)
        self.remove_nesting_level_newlines(pattern)
        self.add_newline_before_elements(pattern)

        return pattern

    def remove_nesting_level_newlines(self, pattern):
        print("********")
        for element_name in list(pattern.keys())[1:]:
            element = pattern[element_name]
            if not isinstance(element, str):
                print(element_name)
                print(element.ca)
                last_item = self.get_last_item(element)
                print(last_item)
                item_keys = list(last_item.ca.items.keys())
                print("lennnn:" + str(len(item_keys)))
                if len(item_keys) > 0 and self.is_empty_comment(last_item.ca.items[item_keys[-1]]):
                    last_item.ca.items[item_keys[-1]] = [None, None, None, None]
                    print("----")
                    print(last_item.ca)
                print("*******")

    def remove_top_level_newlines(self, pattern):
        for top_level_el in list(pattern.ca.items.keys()):
            if self.is_empty_comment(pattern.ca.items[top_level_el]):
                pattern.ca.items[top_level_el] = [None, None, None, None]

    def is_empty_comment(self, comment_attribute):
        """
        Check if all ca items are None or empty strings.
        """
        is_all_empty = True
        for attr in comment_attribute:
            if attr and not str(attr.value):
                is_all_empty = False
        return is_all_empty

    def add_newline_before_elements(self, pattern):
        for element_name in list(pattern.keys())[1:]:
            element = pattern[element_name]
            print(element_name + "  EL Type: " + str(type(element)))
            pattern.yaml_set_comment_before_after_key(element_name, before='\n')

    def get_last_item(self, item):
        if isinstance(item, str):
            return item
        elif isinstance(item, ruamel.yaml.comments.CommentedMap):
            item_keys = list(item.keys())
            print(item_keys)
            if len(item_keys) > 0:
                if isinstance(item[item_keys[-1]], str):
                    print(item[item_keys[-1]])
                    print(item.ca)
                    return item
                else:
                    return self.get_last_item(item[item_keys[-1]])
            else:
                return item
        elif isinstance(item, ruamel.yaml.comments.CommentedSeq):
            print("-1:" + str(item[-1]))
            print(item.ca)
            if isinstance(item[-1], str):
                print(item[-1])
                print(item.ca)
                return item
            else:
                return self.get_last_item(item[-1])
        else:
            print("OOOOOOOOOOO:" + str(type(item)))


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


class CompositeNormaliser(object):

    # normalisers = [ElementOrderNormaliser(), NewLineNormaliser()]
    normalisers = [NewLineNormaliser()]

    def normalise(self, pattern):
        for normalizer in self.normalisers:
            pattern = normalizer.normalise(pattern)
        return pattern


def normalise(input_file, output_file):
    logging.info("Normalising %s" % input_file)
    pattern = read_yaml_file(input_file)
    pattern = CompositeNormaliser().normalise(pattern)
    write_yaml_to_file(pattern, output_file)


def read_yaml_file(input_file):
    ryaml = YAML()
    ryaml.preserve_quotes = True
    pattern = None
    with open(input_file, "r") as stream:
        try:
            pattern = ryaml.load(stream)
        except YAMLError as exc:
            logging.error('Failed to load pattern file: ' + input_file)
    return pattern


def write_yaml_to_file(pattern, output_file):
    ryaml = YAML()
    ryaml.dump(pattern, output_file)
