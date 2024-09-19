#! python3

import os
import sys
import argparse
import re



def main(
    package: str,
    from_manifest: bool,
    path_manifest: str,
    source: str,
    version: str
) -> bool:
    # for all the files that are called code.py in the components folder
    # stamp on the second line of the file by not overwriting the first line
    for root, dirs, files in os.walk(source):
        for file in files:
            if file == "code.py":
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    lines = f.readlines()
                # check if the line # r: package_name is already in the first 10 lines, erase it
                if any([re.search(r"# r: .+==", line) for line in lines[:10]]):
                    print(f"Overwriting file {path}: it was already stamped with the package version.")
                    lines = [line for line in lines if not re.search(r"# r: .+==", line)]

                with open(path, "w") as f:
                    f.write(lines[0])
                    f.write(f"# r: {package}=={version}\n")
                    for line in lines[1:]:
                        f.write(line)
    print("Done stamping components with version number of the pypi package.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add the # r : package==version for ghusers components release."
    )
    parser.add_argument(
        "--package",
        type=str,
        help="The package name."
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        default="./py/components/",
        help="The path to component folders."
    )
    parser.add_argument(
        "--from-manifest",
        action='store_true',
        default=False,
        help="Whether to update the version from the manifest file's version."
    )
    parser.add_argument(
        "--path-manifest",
        type=str,
        required=True,
        default="./manifest.yml",
        help="The path to the manifest file."
    )
    parser.add_argument(
        "--version",
        type=str,
        required=False,
        help="The version number to update and overwrite in the code base."
    )

    args = parser.parse_args()

    if args.package is None:
        parser.print_help()
        sys.exit(1)

    parse_errors = []

    _manifest_version = None
    if args.from_manifest:
        if not os.path.isfile(args.path_manifest):
            parse_errors.append(f"Path to manifest file is invalid: {args.path_manifest}")
        with open(args.path_manifest, "r") as f:
            manifest = f.read()
            match = re.search(r"version: (\d+\.\d+\.\d+)", manifest)
            if match:
                _manifest_version = match.group(1)
        if _manifest_version is None:
            parse_errors.append("Could not find the version number in the manifest file.")
        args.version = _manifest_version
    is_version_ok = True
    _version = args.version
    if not re.match(r"^\d+\.\d+\.\d+$", _version) \
        or _version.count(".") < 2 \
        or len(_version) < 5:
        is_version_ok = False
        parse_errors.append("Version must be in the format: Major.Minor.Patch")

    is_source_populated = True
    if not os.path.isdir(args.source):
        is_source_populated = False
        parse_errors.append(f"Path to source folder is invalid: {args.source}")
    nbr_pycode_files = 0
    for root, dirs, files in os.walk(args.source):
        for file in files:
            if file == "code.py":
                nbr_pycode_files += 1
    if nbr_pycode_files == 0:
        is_source_populated = False
        parse_errors.append(f"Source folder is empty or does not contain components: {args.source}")

    print("Flagerizer checks:")
    if _manifest_version is not None:
        print(f"\t[x] Version from manifest: {_manifest_version}")
    else:
        print(f"\t[ ] Version from manifest: {_manifest_version}")
    if is_version_ok:
        print("\t[x] Correct version format")
    else:
        print("\t[ ] Correct version format")
    if is_source_populated:
        print(f"\t[x] Source folder is populated {args.source} with {nbr_pycode_files} components")
    else:
        print("\t[ ] Source folder is populated")

    if parse_errors.__len__() != 0:
        for error in parse_errors:
            print(error)
        sys.exit(1)

    print("Stamping components with version number of the pypi package:")
    print(f"\t# r: {args.package}=={_version}")

    res = main(
        package=args.package,
        from_manifest=args.from_manifest,
        path_manifest=args.path_manifest,
        source=args.source,
        version=_version
    )

    if res:
        print("[x] Done flagerizing components.")
    else:
        print("[ ] Failed flagerizing components.")
        sys.exit(1)
