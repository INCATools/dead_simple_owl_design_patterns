import os
import glob
import logging
from ruamel.yaml import YAML, YAMLError
from dosdp.document.schema import schema_create_docs
from dosdp.document.pattern import patterns_create_docs, patterns_create_overview


logging.basicConfig(level=logging.INFO)


def generate_schema_documentation(md_location=None):
    """
    Generates md formatted documentation for the schema exists in the dosdp package. An output md_location can be
    optionally identified to specify documentation location or current folder is used by default.
    """
    logging.info("Documenting dosdp schema.")
    if md_location is None:
        md_location = os.getcwd()

    schema_create_docs.generate_schema_documentation(md_output=md_location)


def generate_pattern_documentation(yaml_location, md_location=None, sample_data_dir=None):
    """
    Creates md formatted documentation for the given pattern file in the given location.

    Args:
         yaml_location: pattern file location
         md_location: If the yaml_location is a directory, expects md_location parameter to be a folder as well
         and creates documentation in it. If the yaml_location is a file, md_location can be a folder or file.
         If md_location is not given at all, documentation is generated next to the pattern file.
         sample_data_dir: Optional parameter for the sample date folder to read sample tabular data.
    """
    logging.info("Documenting pattern file: " + yaml_location)
    if md_location is None:
        if yaml_location.endswith(".yaml"):
            md_location = str(yaml_location).split(".yaml")[0] + ".md"
        else:
            md_location = str(yaml_location).split(".yml")[0] + ".md"

    if os.path.isdir(yaml_location):
        if not yaml_location.endswith(os.path.sep):
            yaml_location += os.path.sep
        pattern_docs = glob.glob(yaml_location + "*.yaml")
        pattern_docs.extend(glob.glob(yaml_location + "*.yml"))
        if not os.path.isdir(md_location):
            logging.error("If input parameter is a folder, output parameter also should be a folder.", )
        else:
            for pattern_doc in pattern_docs:
                create_indv_pattern_doc(pattern_doc, md_location, sample_data_dir)
            patterns_create_overview.create_overview(yaml_location,
                                                     md_file=os.path.join(md_location, "overview.md"),
                                                     matches_dir=sample_data_dir)
    elif yaml_location.endswith('.yaml') or yaml_location.endswith('.yml'):
        create_indv_pattern_doc(yaml_location, md_location, sample_data_dir)
    else:
        logging.error("Given path has unsupported file extension:", yaml_location)


def create_indv_pattern_doc(yaml_location, md_location, sample_data_dir=None):
    if patterns_create_docs.is_dosdp_pattern_file(yaml_location):
        if os.path.isdir(md_location):
            file_name = os.path.basename(yaml_location)
            md_location = os.path.join(md_location, (os.path.splitext(file_name)[0] + ".md"))
        patterns_create_docs.generate_pattern_documentation(yaml_location, md_location, sample_data_dir)
    else:
        logging.warning("File is not a pattern file, skipping: " + yaml_location)
