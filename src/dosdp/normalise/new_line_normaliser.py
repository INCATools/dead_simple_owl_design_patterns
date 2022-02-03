import logging
import ruamel.yaml
from dosdp.normalise.base_normaliser import BaseNormaliser


logging.basicConfig(level=logging.INFO)


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
        Check if all ca items are None and empty strings.
        """
        is_all_empty = True
        for attr in comment_attribute:
            if attr and str(attr.value).replace("\n", ""):
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
            raise ValueError("Unsupported construct in newline normalisation: " + str(type(item)))

