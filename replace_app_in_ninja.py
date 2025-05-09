import argparse
import os
import re
import shutil
import sys
from typing import Optional 

def replace_library_in_ninja(ninja_filepath, old_lib_string, new_lib_string, output_filepath=None):
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

    if output_filepath is None:
        # In-place modification with backup
        backup_filepath = ninja_filepath + ".bak"
        try:
            shutil.copy2(ninja_filepath, backup_filepath)
            print(f"Backed up original file '{ninja_filepath}' to '{backup_filepath}'")
        except Exception as e:
            print(f"Error creating backup for '{ninja_filepath}': {e}", file=sys.stderr)
            return False
        current_target_filepath = ninja_filepath
    else:
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
    print(f"Replacing all occurrences of '{old_lib_string}' with '{new_lib_string}'")

    try:
        with open(ninja_filepath, 'r') as f_in:
            found_app_block = False
            app_regex = r"build.*CMakeFiles.*main.cc.obj"

            for line_num, line_content in enumerate(f_in, 1):
                original_line = line_content
                # Perform global replacement on the current line
                # rstrip is not used here to preserve original line endings as much as possible
                # if line_content[-1] == '\n': ends_with_newline = True else: ends_with_newline = False
                # modified_line_content = line_content.rstrip('\n\r').replace(old_lib_string, new_lib_string)
                modified_line_content = line_content.replace(old_lib_string, new_lib_string)


                if modified_line_content != original_line:
                    num_replacements_in_line = original_line.count(old_lib_string)
                    changes_made_count += num_replacements_in_line
                    if num_replacements_in_line > 0 : # ensure line was actually affected by this specific replacement
                        lines_affected_count +=1
                    # print(f"  L{line_num}: Modified ({num_replacements_in_line} occurrence(s) replaced)")
                
                if not found_app_block and re.search(app_regex, line_content):
                    print(line_content)
                    found_app_block = True
                    continue
                elif line_content == "\n" and found_app_block:
                    print(line_content)
                    print("-- Done skipping app block")
                    found_app_block = False
                    continue
                elif found_app_block:
                    print(line_content)
                    continue
                    
                modified_lines.append(modified_line_content)

        if changes_made_count > 0:
            print(f"\nTotal occurrences replaced: {changes_made_count} across {lines_affected_count} line(s).")
            print(f"Writing modified content to '{current_target_filepath}'...")
            with open(current_target_filepath, 'w', encoding='utf-8') as f_out:
                for line in modified_lines:
                    f_out.write(line) # Write line as is (should include its original newline)
            print("Modification complete.")
        else:
            print(f"\nNo occurrences of '{old_lib_string}' found for replacement in the file.")
            if output_filepath is None and os.path.exists(backup_filepath):
                print(f"No changes made, removing backup file: '{backup_filepath}'")
                os.remove(backup_filepath)
            elif output_filepath is not None and output_filepath != ninja_filepath:
                print(f"Output file '{output_filepath}' will be identical to input as no replacements occurred.")
                # Still write it to conform to expectation if an output file was specified
                with open(current_target_filepath, 'w', encoding='utf-8') as f_out:
                    for line in modified_lines:
                        f_out.write(line)
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
    parser.add_argument('--old_library',
                        '-l',
                        help="The exact string of the old library to replace "
                             "(e.g., 'libs/libold.a', 'old.lib').\n"
                             "This must be how it appears in the Ninja "
                             "file's input lists.")
    parser.add_argument('--app_library',
                        '-a',
                        help="The exact string of the new library to use "
                        "(e.g., 'external/libnew.a', 'new.lib').")
    parser.add_argument("-o", "--output-file",
                        help="Path to write the modified Ninja file. \n"
                             "If not provided, modifies the input file in-place (a .bak backup will be created).",
                        default=None)
    return parser

def main():
    args = arg_parser().parse_args()
    if not replace_library_in_ninja(
            args.ninja_file, 
            args.old_library, 
            args.app_library,
            args.output_file):
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
