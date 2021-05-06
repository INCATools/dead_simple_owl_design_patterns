import argparse
import sys
import pathlib
from dosdp import validator
from dosdp import document


def main():
    parser = argparse.ArgumentParser(prog="dosdp", description='DOS-DP exchange format cli interface.')
    subparsers = parser.add_subparsers(help='Available dosdp actions', dest='action')

    parser_validate = subparsers.add_parser("validate",
                                            description="The validate parser",
                                            help="Validates given argument if it is a yaml/yaml file. If argument is a "
                                                 "folder, validates all pattern files located in the given directory.")
    parser_validate.add_argument('-i', '--input', action='store', type=pathlib.Path, required=True)

    parser_document = subparsers.add_parser("document", add_help=False,
                                            description="The document generation parser",
                                            help="Generates documentation for the given YAML schema.")
    parser_document.add_argument('-i', '--input', action='store', type=pathlib.Path, required=True)
    parser_document.add_argument('-o', '--output', action='store', type=pathlib.Path, required=True)

    args = parser.parse_args()

    if args.action == "validate":
        is_valid = validator.validate(str(args.input))
        if not is_valid:
            sys.exit(1)
    elif args.action == "document":
        document.generate_documentation(str(args.input), str(args.output))


if __name__ == "__main__":
    main()
