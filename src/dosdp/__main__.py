import argparse
import sys
from validator import validate


def main():
    parser = argparse.ArgumentParser(prog='dosdp', description='Validates DOSDP pattern files.')
    parser.add_argument('-v', '--validate', action='store', type=str, required=True,
                        help='Validates given argument if it is a yaml/yaml file. If argument is a folder, validates '
                             'all pattern files located in the given directory.')
    args = parser.parse_args()

    if args.validate:
        is_valid = validate(args.validate)

        if not is_valid:
            sys.exit(1)


if __name__ == "__main__":
    main()
