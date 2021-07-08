import jsonschema2md
import os
import logging
import yaml
import configparser
from ruamel.yaml import YAML, YAMLError

NESTED_REFERENCE_LIMIT = 3

DEFINITION_PREFIX = "def_"

CROSS_REF_TERM = "Refer to *#/definitions/"
CROSS_REF_TERM_ALT = "Values from *"

logging.basicConfig(level=logging.INFO)

DOSDP_SCHEMA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../schema/dosdp_schema.yaml")
DOSDP_SCHEMA_MD = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../schema/dosdp_schema.md")
DOSDP_DOCUMENTATION_CONF = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                        "../../../schema/dosdp_schema_doc.ini")


def generate_plain_documentation(yaml_schema, mapping_definitions):
    """
    Generates a plain documentation using jsonschema2md library.

    Returns: Dictionary of element documentations. Key is element name and value is list of documentation lines.
    """
    parser = jsonschema2md.Parser()

    with open(yaml_schema, 'r') as yaml_in:
        dosdp = yaml.safe_load(yaml_in)
        md_lines = parser.parse_schema(dosdp)

        plain_documentation = dict()
        element_lines = []
        element_name = ""

        is_definition = False
        element_path = list()
        prev_indent = 0
        curr_indent = 0
        for line in md_lines:
            if line.startswith("## Definitions"):
                is_definition = True
            elif line.startswith("## Properties"):
                is_definition = False

            line = line.replace("\n", "")

            if line.startswith("- **`"):
                if element_name:
                    plain_documentation[element_name] = element_lines
                element_name = get_element_name(is_definition, line)
                element_path = [element_name]
                line = insert_mapping_definition(element_path, line, mapping_definitions)
                element_lines = [line]
                curr_indent = 0
            elif line and not line.startswith("#"):
                prev_indent = curr_indent
                curr_indent = len(line) - len(line.lstrip(' '))
                if curr_indent == prev_indent:
                    element_path.remove(element_path[-1])
                elif curr_indent <= prev_indent:
                    element_path.remove(element_path[-1])
                    element_path.remove(element_path[-1])
                element_path.append(get_element_name(False, line))

                line = insert_mapping_definition(element_path, line, mapping_definitions)
                element_lines.append(line)

        plain_documentation[element_name] = element_lines
        handle_one_of_definitions(plain_documentation)

        return plain_documentation


def insert_mapping_definition(element_path, line, mapping_definitions):
    """
    Inserts mapping definition to the element description if required. Otherwise, returns the line as is.
    """
    if "$".join(element_path).replace("def_", "").lower() in mapping_definitions:
        if "*:" in line:
            parts = line.split("*:")
            line = parts[0] + "*:" + " Mapped to `" + \
                   mapping_definitions["$".join(element_path).replace("def_", "").lower()] + "`. " + parts[1]
    return line


def get_element_name(is_definition, line):
    """
    Extract element name from jsonschema2md generated documentation line.
    """
    first_occur = line.index("**")
    second_occur = line.index("**", first_occur + 1)
    element_name = line[first_occur + 2:second_occur]
    if "`" in element_name:
        element_name = element_name.replace("`", "").strip()
    if is_definition:
        element_name = DEFINITION_PREFIX + element_name

    return element_name


def find_mapping_definitions():
    """
    'Mapping' definitions are not handled by the jsonschema2md. To manually add documentation for these definitions,
    searches for all mapping definitions in the schema.

    Return: Dictionary of mapping definitions. Key is path of the mapping element,
    value is value of the mapping definition.
    """
    mapping_definitions = dict()
    ryaml = YAML(typ='safe')
    with open(DOSDP_SCHEMA, "r") as stream:
        try:
            content = ryaml.load(stream)
            path = list()
            scan_element_for_mapping(content, mapping_definitions, path)
        except YAMLError:
            logging.error('Failed to load pattern file: ' + DOSDP_SCHEMA)

    return mapping_definitions


def scan_element_for_mapping(element, mapping_definitions, path):
    """
    Recursively scans schema to identify mapping definitions. Fills the mapping definitions dictionary.
    """
    for key in element.keys():
        path.append(key)
        if "mapping" == key:
            path_refine = path[0:len(path) - 1]
            if "definitions" in path_refine: path_refine.remove("definitions")
            if "properties" in path_refine: path_refine.remove("properties")
            mapping_definitions["$".join(path_refine)] = element["mapping"]
        elif isinstance(element[key], dict):
            scan_element_for_mapping(element[key], mapping_definitions, path)
        path.remove(key)


def handle_one_of_definitions(plain_documentation):
    """
    'OneOf' definitions are not handled by the jsonschema2md. Manually adding documentation for these definitions.
    """
    ryaml = YAML(typ='safe')
    with open(DOSDP_SCHEMA, "r") as stream:
        try:
            content = ryaml.load(stream)
            definitions = content["definitions"]
            for key in definitions.keys():
                if "oneOf" in definitions[key]:
                    one_of_defs = definitions[key]["oneOf"]
                    if "$ref" in one_of_defs[0]:
                        element_lines = ["- **`annotations`** *(array)*: One of the followings:"]
                        for one_of_item in one_of_defs:
                            element_lines.append("  - **Items**: Refer to *" + one_of_item["$ref"] + "*.")
                        plain_documentation[DEFINITION_PREFIX + key] = element_lines
        except YAMLError as exc:
            logging.error('Failed to load pattern file: ' + DOSDP_SCHEMA)


def print_documentation_header(doc_type_elements, config, md_out):
    """
    Adds headings and table of contents to the documentation.
    """
    md_out.write("# %s\n" % doc_type_elements["doc_title"])
    md_out.write("\n")

    print_documentation_toc(config, md_out)

    md_out.write("\n")
    md_out.write("## %s\n" % "Properties")
    md_out.write("\n")


def print_documentation_toc(config, md_out):
    """
    Prints table of contents based on documentation config.
    """
    sections = config.sections()
    for section in sections:
        section_config = config[section]
        if section == "root":
            md_out.write("- [" + section_config["title"] + "](#" +
                         section_config["title"].lower().replace(" ", "-") + ")\n")
        else:
            md_out.write("  * [" + section_config["title"] + "](#" +
                         section_config["title"].lower().replace(" ", "-") + ")\n")


def print_element(element, md_out, plain_doc, prefix="", nesting_list=[], in_reference=False):
    """
    Retrieves plain element documentation generated by the jsonschema2md and writes to the document.
    Additionally expands 'definitions' references to a specified depth (see NESTED_REFERENCE_LIMIT)
    in order to prevent indefinite circular references.
    """
    # prefix = ">" * (len(nesting_list))
    indentation = prefix + ("  " * (len(nesting_list) % 2))
    lines = plain_doc[element]

    # postpone writing references (as last items) to make it more readable
    reference_defs = list()
    reference_elements = dict()
    is_annotation = False
    for count, line in enumerate(lines):
        line = customize_doc_content(line)

        if "**`annotations`** *(list)*" in line:
            reference_definition = indentation + line
            reference_defs.append(reference_definition)
            reference_elements[reference_definition] = list()
            is_annotation = True
        elif CROSS_REF_TERM_ALT in line:
            nesting_list.append(element)
            ref_term_start = line.index(CROSS_REF_TERM_ALT) + len(CROSS_REF_TERM_ALT)
            referred_element = line[ref_term_start:len(line) - 2]
            if is_annotation:
                reference_elements[reference_defs[-1]].append(DEFINITION_PREFIX + referred_element)
            else:
                if "- **Items**" not in line:
                    md_out.write("%s\n" % (indentation + line.split(CROSS_REF_TERM_ALT)[0].rstrip()))
                    # md_out.write("%s\n" % (indentation + line))
                if (DEFINITION_PREFIX + referred_element) not in nesting_list:
                    print_element(DEFINITION_PREFIX + referred_element, md_out, plain_doc,
                                  "" if len(nesting_list) == 1 else indentation + "  ", nesting_list)
                else:
                    # ellipsis to indicate recursion
                    md_out.write("%s\n" % (indentation + " " * (len(line) - len(line.lstrip())) + "  - ..."))
        else:
            is_annotation = False
            if not (element.startswith(DEFINITION_PREFIX) and count == 0 and not in_reference) \
                    and "- **Items**" not in line and "_annotation`** *(object)*:" not in line:
                md_out.write("%s\n" % (indentation + line))

    for count, reference in enumerate(reference_defs):
        if "**`annotations`** *(list)*: One of the followings:" in reference:
            md_out.write("%s\n" % (indentation + "*Use one of the followings:*"))
        else:
            md_out.write("%s\n" % reference)
        for element in reference_elements[reference]:
            if element not in nesting_list:
                md_out.write("\n")
                print_element(element, md_out, plain_doc,
                              prefix if prefix.startswith(">") else ">" + prefix, nesting_list, in_reference=True)
            else:
                # ellipsis to indicate recursion
                line_content = reference.replace(">", "")
                md_out.write("%s\n" % (indentation + " " * (len(line_content) - len(line_content.lstrip())) + "  - ..."))


def customize_doc_content(line):
    """
    Place content customizations to here. Such as don't display "array", use "list instead"
    """
    if "*(array)*" in line:
        line = line.replace("*(array)*", "*(list)*")

    if "*(array)*" in line:
        line = line.replace("*(object)*", "*(dict)*")

    if CROSS_REF_TERM in line:
        line = line.replace(CROSS_REF_TERM, CROSS_REF_TERM_ALT)

    return line


def print_section_header(config, md_out, section):
    """
    Adds a section title and description for doc_type.
    'root' doc_type is a special type and doesn't have a title and description.
    """
    if not section == "root":
        section_config = config[section]
        md_out.write("### %s\n" % section_config["title"])
        md_out.write("\n")
        md_out.write("%s\n" % section_config["description"])
        md_out.write("\n")


def get_doc_type_elements():
    """
    Reads the schema file and builds a list of doc_type elements.

    Returns: dictionary of schema elements. Key is doc_type (as defined in the ini config)
    and value is list of element names.
    """
    doc_type_elements = dict()

    ryaml = YAML(typ='safe')
    with open(DOSDP_SCHEMA, "r") as stream:
        try:
            content = ryaml.load(stream)
            doc_type_elements["doc_title"] = content["title"]
            properties = content["properties"]

            for key in properties.keys():
                doc_type = properties[key]["doc_type"]
                if doc_type in doc_type_elements:
                    doc_type_elements[doc_type].append(key)
                else:
                    doc_type_elements[doc_type] = [key]
        except YAMLError as exc:
            logging.error('Failed to load pattern file: ' + DOSDP_SCHEMA)
    return doc_type_elements


def generate_schema_documentation(yaml_schema=DOSDP_SCHEMA, md_output=DOSDP_SCHEMA_MD):
    """
    Generates documentation for the given YAML schema. Uses jsonschema2md to generate a plain documentation,
    then decorates generated documentation through using the documentation config (.ini file)
    """
    mapping_definitions = find_mapping_definitions()
    plain_doc = generate_plain_documentation(yaml_schema, mapping_definitions)

    config = configparser.ConfigParser()
    config.read(DOSDP_DOCUMENTATION_CONF)
    sections = config.sections()

    doc_type_elements = get_doc_type_elements()

    if os.path.isdir(md_output):
        file_name = os.path.basename(yaml_schema)
        md_output = os.path.join(md_output, (os.path.splitext(file_name)[0] + ".md"))

    logging.info("Target is: " + os.path.abspath(md_output))
    with open(md_output, "w") as md_out:
        print_documentation_header(doc_type_elements, config, md_out)

        for section in sections:
            elements = doc_type_elements[section]
            print_section_header(config, md_out, section)

            for element in elements:
                print_element(element, md_out, plain_doc, nesting_list=[])
                md_out.write("\n\n")


# generate_schema_documentation(DOSDP_SCHEMA)
