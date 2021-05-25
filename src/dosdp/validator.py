#!/usr/bin/env python3
import glob
import re
import warnings
import os
import logging
from jsonschema import Draft7Validator
from jsonpath_rw import parse
from ruamel.yaml import YAML, YAMLError

logging.basicConfig(level=logging.INFO)


def test_jschema(validator, pattern):
    """
    Validates if given schema is a valid json schema.
    Args:
        validator: sjon schema validator
        pattern: schema in yaml format to validate

    Returns: True if schema is valid, False otherwise.
    """
    is_valid = True

    if not validator.is_valid(pattern):
        es = validator.iter_errors(pattern)
        for e in es:
            warnings.warn(" => ".join([str(e.schema_path), str(e.message), str(e.context)]))
            is_valid = False

    return is_valid



def test_vars(pattern):
    """
    Tests whether variable names in any field with key 'vars' is in the vars list for the pattern
    Args:
         pattern: schema in yaml format to validate

    Returns: True if schema vars are valid, False otherwise.
    """
    if 'vars' in pattern.keys():
        vars = set(pattern['vars'].keys())
    else:
        warnings.warn("Pattern has no vars")
        return True ## If this is to be compulsory, should be spec'd as such in json_schema
    if 'data_vars' in pattern.keys():
        vars.update(set(pattern['data_vars'].keys()))
    if 'substitutions' in pattern.keys():
        subvars = [X['out'] for X in pattern['substitutions']]
        vars.update(set(subvars))       
    expr = parse('*..vars')
    var_fields = [match for match in expr.find(pattern)]
    stat = True
    if var_fields:
        for field in var_fields:
            val = set(field.value)
            if not vars.issuperset(val):
                warnings.warn("%s has values (%s) not found in pattern variable list (%s): "
                  % (field.full_path, str(val.difference(vars)), str(vars)))
                stat = False
    else:
        warnings.warn("Pattern has no var fields")
    return stat


def test_text_fields(pattern):
    """
    Structurally tests whether quotations match and declared values exist in owl entity dictionaries.
     Args:
         pattern: schema in yaml format to validate

    Returns: True if schema text fields are valid, False otherwise.
    """
    owl_entities = set()
    if 'classes' in pattern.keys(): owl_entities.update(set(pattern['classes'].keys()))
    if 'relations' in pattern.keys(): owl_entities.update(set(pattern['relations'].keys()))
    expr = parse('logical_axioms.[*].text')
    ms_fields = [match for match in expr.find(pattern)]
    expr = parse('equivalentTo|subClassOf|GCI|disjointWith.text')
    ms_fields.extend([match for match in expr.find(pattern)])
    stat=True
    if ms_fields:
        for field in ms_fields:
            # Test for even number single quotes
            val = field.value
            m = re.findall("'", val)
            if divmod(len(m), 2)[1]:
                warnings.warn("text field '%s' has an odd number of single quotes." % val)
                stat = False
            # Test that single quoted strings are OWL entities in dict.
            m = re.findall("'(.+?)'", val)
            quoted = set(m)
            if not owl_entities.issuperset(quoted):
                warnings.warn("%s has values (%s) not found in owl entity dictionaries t (%s): "
                  % (field.full_path, str(quoted.difference(owl_entities)), str(owl_entities)))
                stat = False
    else:
        warnings.warn("Pattern has no text fields")
    return stat


def format_warning(message, category, filename, lineno, line=None):
    return '%s:%s: %s:%s\n' % (filename, lineno, category.__name__, message)


def validate(pattern):
    """
    If given parameter is a yaml/yaml file, validates it. If parameter is a folder, validates all pattern files located
    in the given path.
    Args:
    pattern: path to a yaml file or path to directory with pattern files in yaml. Files must have the extension .yaml or .yml.
    All files in directory with these extensions are assumed to be dosdp pattern files.

    Returns: True if patterns are valid, False otherwise.
    """
    schema_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../schema/dosdp_schema.yaml")
    ryaml = YAML(typ='safe')

    dosdp = None
    with open(schema_path) as stream:
        try:
            dosdp = ryaml.load(stream)
        except YAMLError as exc:
            logging.error('Failed to open dosdp schema: ' + schema_path)

    validator = Draft7Validator(dosdp)

    warnings.formatwarning = format_warning
    if os.path.isdir(pattern):
        if not pattern.endswith(os.path.sep):
            pattern += os.path.sep
        pattern_docs = glob.glob(pattern + "*.yaml")
        pattern_docs.extend(glob.glob(pattern + "*.yml"))
    elif pattern.endswith('.yaml') or pattern.endswith('.yaml'):
        pattern_docs = [os.path.abspath(pattern)]
    else:
        logging.error("Given path has unsupported file extension.", )

    stat = True
    for pattern_doc in pattern_docs:
        logging.info("Checking %s" % pattern_doc)
        with open(pattern_doc, "r") as stream:
            try:
                pattern = ryaml.load(stream)
                if not test_jschema(validator, pattern): stat = False
                if not test_vars(pattern): stat = False
                if not test_text_fields(pattern): stat = False
            except YAMLError as exc:
                stat = False
                logging.error('Failed to load pattern file: ' + pattern_doc)
            except AttributeError as exc:
                stat = False
                logging.error('Unexpected pattern file content: ' + pattern_doc)
                logging.error(exc)
    if stat:
        logging.info("Validation completed without any issues to report.")
    else:
        logging.info("Validation completed with issues to be fixed.")

    return stat
