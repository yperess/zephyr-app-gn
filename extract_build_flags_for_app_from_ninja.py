"""
 EX:  python extract_build_flags_for_app_from_ninja.py -n out/build.ninja -a "app" -o test.gn 
"""
import argparse
import os
import re
import shutil
import sys
from typing import Optional 

def parse_defines(line):
    return_string = "config(\"defines\") {\n  defines = [\n"
    defines = line.split()
    for define in defines[2:]:
        return_string += "    \"" + define[2:] + "\",\n"
    return_string += "  ]\n}\n\n"
    return return_string

def parse_flags(line):
    return_string = "config(\"flags\") {\n  cflags_c = [\n"
    flags = line.split()

    flag_string = ""
    for flag in flags[2:]:
        # Handle flags with arguments
        if flag[0] != '-':
            return_string = return_string[:-3]
            return_string += " " + flag + "\",\n"
        elif "-fmacro-prefix-map" in flag:
            continue
        else:
            return_string += "    \"" + flag + "\",\n"

    return_string += "  ]\n}\n\n"
    return return_string

def parse_includes(line):
    return_string = "config(\"public_includes\") {\n  include_dirs = [\n"
    includes = line.split()
    for include in includes [2:]:
        if "isystem" in include or include[0] != '-':
            continue

        if include[-1] == '.':
            return_string += "    \"" + include[2:-2] + "\",\n"
        else:
            return_string += "    \"" + include[2:] + "\",\n"

    return_string += "  ]\n}\n\n"
    return return_string
    return

def extract_build_flags_for_app_from_ninja(ninja_filepath, app_string, output_filepath):
    """
    Reads a Ninja build file, replaces occurrences of old_lib_str with 
    new_lib_str in the input dependencies of build statements, and writes the 
    output.

    Args:
        ninja_filepath (str): Path to the input build.ninja file.
        old_lib_str (str): The exact string of the old library to replace.
        new_lib_str (str): The exact string of the new library to use.
        output_filepath (str, optional): Path to write the modified file.
                                         If None, modifies in-place with a backup.
    """
    if not os.path.exists(ninja_filepath):
        print(f"Error: Input file not found: {ninja_filepath}", file=sys.stderr)
        return False

    # Writing to a new output file
    current_target_filepath = output_filepath
    output_dir = os.path.dirname(output_filepath)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating output directory '{output_dir}': {e}", file=sys.stderr)
            return False

    modified_lines = []
    changes_made_count = 0
    lines_affected_count = 0

    print(f"Processing '{ninja_filepath}'...")

    try:
        defines = ""
        flags = ""
        includes = ""

        with open(ninja_filepath, 'r') as f_in:
            app_regex = r"build CMakeFiles.*main.*obj:"
            found_app_block = False
             
            for line_num, line_content in enumerate(f_in, 1):
                if not found_app_block and re.search(app_regex, line_content):
                    found_app_block = True
                if line_content == "\n" and found_app_block:
                    break
                if found_app_block and "DEFINES = " in line_content:
                    defines = parse_defines(line_content)
                if found_app_block and "FLAGS = " in line_content:
                    flags = parse_flags(line_content)
                if found_app_block and "INCLUDES =" in line_content:
                    includes = parse_includes(line_content)

        print(f"Output file '{output_filepath}'.")
        # Still write it to conform to expectation if an output file was specified
        with open(current_target_filepath, 'w', encoding='utf-8') as f_out:
            f_out.write(includes)
            f_out.write(defines)
            f_out.write(flags)

        return True

    except Exception as e:
        print(f"An error occurred during processing: {e}", file=sys.stderr)
        return False

def arg_parser(
    parser: Optional[argparse.ArgumentParser] = None
) -> argparse.ArgumentParser:
    if parser is None:
        parser = argparse.ArgumentParser(
            description="Replace a library with another in a Ninja build file. "
                        "WARNING: Directly modifying auto-generated Ninja files"
                        "is risky and changes may be overwritten by your "
                        "meta-build system (e.g., GN, CMake). "
                        "Use with extreme caution.",
            formatter_class=argparse.RawTextHelpFormatter
        )

    parser.add_argument('--ninja_file', 
                        '-n',
                        help="Path to the input build.ninja file.")
    parser.add_argument('--app',
                        '-a',
                        help="The exact string of the new library to use "
                        "(e.g., 'external/libnew.a', 'new.lib').")
    parser.add_argument("-o", "--output-file",
                        help="Path to write the modified Ninja file. \n"
                             "If not provided, modifies the input file in-place (a .bak backup will be created).")
    return parser


def main():
    args = arg_parser().parse_args()
    if not extract_build_flags_for_app_from_ninja(
            args.ninja_file, 
            args.app,
            args.output_file):
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
