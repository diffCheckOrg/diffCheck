#! python3

import os
import sys
import argparse

import typing

def main(
    setup_path: str,
    *args, **kwargs
) -> bool:
    setup_dir = os.path.dirname(setup_path)
    os.chdir(setup_dir)
    try:
        os.system(f"python setup.py sdist")
        os.system(f"python setup.py bdist_wheel")
    except Exception as e:
        print(f"Failed to build the package: {e}")
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build the python package and wheel."
    )
    parser.add_argument(
        "--setup-path",
        type=str,
        required=True,
        default="./py/pypi/setup.py",
        help="The path to the setup file of the python package."
    )

    args = parser.parse_args()
    parse_errors = []

    is_setup_path_correct = True
    if not os.path.isfile(args.setup_path):
        parse_errors.append(f"Path to setup file is invalid: {args.setup_path}")
        is_setup_path_correct = False

    print("Pypireize  check:")
    if is_setup_path_correct:
        print(f"\t[x] Setup file path: {args.setup_path}")
    else:
        print(f"\t[ ] Setup file path: {args.setup_path}")
    if parse_errors:
        for error in parse_errors:
            print(error)
        sys.exit(1)
    print("Starting the pypireize task...")

    res = main(
        setup_path=args.setup_path
    )
    if res:
        print("[x] Pypireize task completed.")
    else:
        print("[ ] Pypireize task failed.")
        sys.exit(1)
