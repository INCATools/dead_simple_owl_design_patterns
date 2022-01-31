import argparse
import sys
import pathlib
import logging
from dosdp import validator
from dosdp.document import document
from dosdp.normalise import normalizer

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(prog="dosdp", description='DOS-DP exchange format cli interface.')
    subparsers = parser.add_subparsers(help='Available dosdp actions', dest='action')

    add_validate_parser(subparsers)
    add_document_parser(subparsers)
    add_normalise_parser(subparsers)

    args = parser.parse_args()

    if args.action == "validate":
        is_valid = validator.validate(str(args.input))
        if not is_valid:
            sys.exit(1)
    elif args.action == "document":
        if 'schema' in args and args.schema:
            document.generate_schema_documentation(args.output)
        elif 'input' in args:
            document.generate_pattern_documentation(str(args.input), args.output, args.data)
        else:
            logging.error("Please use '--schema' to generate schema documentation "
                          "or '--input' for pattern documentation.")
    elif args.action == "normalise":
        normalizer.normalise(args.input, args.output)


def add_normalise_parser(subparsers):
    parser_normalise = subparsers.add_parser("normalise", add_help=False,
                                             description="The template normalisation parser",
                                             help="Normalises format of the given DOSDP schema.")
    parser_normalise.add_argument('-i', '--input', action='store', type=pathlib.Path, required=True)
    parser_normalise.add_argument('-o', '--output', action='store', type=pathlib.Path)


def add_document_parser(subparsers):
    parser_document = subparsers.add_parser("document", add_help=False,
                                            description="The document generation parser",
                                            help="Generates documentation for the given YAML schema.")
    parser_document.add_argument('-s', '--schema', action='store_true')
    parser_document.add_argument('-i', '--input', action='store', type=pathlib.Path)
    parser_document.add_argument('-o', '--output', action='store', type=pathlib.Path)
    parser_document.add_argument('-d', '--data', action='store', type=pathlib.Path)


def add_validate_parser(subparsers):
    parser_validate = subparsers.add_parser("validate",
                                            description="The validate parser",
                                            help="Validates given argument if it is a yaml/yaml file. If argument is a "
                                                 "folder, validates all pattern files located in the given directory.")
    parser_validate.add_argument('-i', '--input', action='store', type=pathlib.Path, required=True)


if __name__ == "__main__":
    main()
