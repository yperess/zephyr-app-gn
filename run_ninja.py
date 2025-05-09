import argparse
import subprocess
import sys
import os
import shutil
from typing import Optional 

def find_ninja_executable():
    ninja_exec = shutil.which("ninja")
    if ninja_exec:
        return ninja_exec
    
    return None


def run_ninja_build(build_directory, targets=None, jobs=None, verbose=False, clean_first=False):
    """
    Runs a Ninja build command.

    Args:
        build_directory (str): The directory containing the build.ninja file.
        targets (list, optional): A list of specific targets to build. Defaults to None (build default targets).
        jobs (int, optional): Number of parallel jobs for Ninja (-j N). Defaults to None.
        verbose (bool, optional): Enable verbose output from Ninja (-v). Defaults to False.
        clean_first (bool, optional): Run 'ninja clean' before building. Defaults to False.

    Returns:
        bool: True if the build was successful, False otherwise.
    """
    ninja_exec = find_ninja_executable()
    if not ninja_exec:
        print("Error: Ninja executable not found. Please ensure 'ninja' is in your PATH or provide the path via --ninja-path.", file=sys.stderr)
        return False

    if not os.path.isdir(build_directory):
        print(f"Error: Build directory '{build_directory}' not found.", file=sys.stderr)
        return False

    if clean_first:
        clean_command = [ninja_exec, "-C", build_directory, "clean"]
        print(f"Executing clean command: {' '.join(clean_command)}")
        try:
            clean_result = subprocess.run(clean_command, check=True)
            print("Clean command successful.")
        except FileNotFoundError:
            print(f"Error: Ninja executable '{ninja_exec}' not found during clean.", file=sys.stderr)
            return False
        except subprocess.CalledProcessError as e:
            print(f"Error: Ninja clean command failed with exit code {e.returncode}.", file=sys.stderr)
            if e.stdout:
                print(f"Clean stdout:\n{e.stdout.decode(errors='ignore')}", file=sys.stderr)
            if e.stderr:
                print(f"Clean stderr:\n{e.stderr.decode(errors='ignore')}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"An unexpected error occurred during ninja clean: {e}", file=sys.stderr)
            return False


    base_command = [ninja_exec, "-C", build_directory]

    if jobs is not None:
        base_command.extend(["-j", str(jobs)])

    if verbose:
        base_command.append("-v")
        
    if targets:
        base_command.extend(targets)
    else:
        # If no specific targets, Ninja builds the default targets.
        # Some projects might require 'all' explicitly if no default is set up well.
        # For most well-configured Ninja builds, no target means "default".
        pass


    print(f"Executing build command: {' '.join(base_command)}")

    try:
        # Run the command. Output will go to stdout/stderr of this script.
        # Using check=True will raise CalledProcessError if ninja returns a non-zero exit code.
        result = subprocess.run(base_command, check=True)
        print("\nNinja build successful.")
        return True
    except FileNotFoundError:
        print(f"Error: Ninja executable '{ninja_exec}' not found.", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as e:
        print(f"\nError: Ninja build failed with exit code {e.returncode}.", file=sys.stderr)
        # stdout and stderr are already printed to console by subprocess.run
        # unless capture_output=True was used.
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return False

def arg_parser(
    parser: Optional[argparse.ArgumentParser] = None
) -> argparse.ArgumentParser:
    if parser is None:
        parser = argparse.ArgumentParser(description="Run a Ninja build.",
            formatter_class=argparse.RawTextHelpFormatter
        )
    
    parser.add_argument("build_directory",
                        help="The directory containing the build.ninja file (e.g., 'out/Release').")
    parser.add_argument("targets", nargs="*",
                        help="Optional. Specific targets to build (e.g., 'my_executable my_library'). "
                             "If not provided, Ninja builds default targets.")
    parser.add_argument("-j", "--jobs", type=int,
                        help="Optional. Number of parallel jobs to run (passed to ninja -j).")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Optional. Enable verbose output from Ninja (ninja -v).")
    parser.add_argument("-c", "--clean", action="store_true",
                        help="Optional. Run 'ninja clean' in the build directory before building.")

    return parser

def main():
    args = arg_parser().parse_args()
    
    print(f"--- Python Ninja Build Runner ---")
    print(f"Build directory: {args.build_directory}")
    if args.targets:
        print(f"Targets: {', '.join(args.targets)}")
    if args.jobs:
        print(f"Jobs: {args.jobs}")
    if args.verbose:
        print(f"Verbose: True")
    if args.clean:
        print(f"Clean first: True")
    print("-" * 30)


    if run_ninja_build(args.build_directory,
                       args.targets,
                       args.jobs,
                       args.verbose,
                       args.clean):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
