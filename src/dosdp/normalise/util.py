import logging
from ruamel.yaml import YAML, YAMLError

logging.basicConfig(level=logging.INFO)


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
    ryaml.width = 2048
    ryaml.dump(pattern, output_file)