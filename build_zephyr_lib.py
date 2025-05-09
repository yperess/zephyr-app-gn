"""Run Zephyr ninja target(s)"""
import subprocess
import sys
import argparse


def main():
    """Run a ninja job"""
    parser = argparse.ArgumentParser(
        description="A sample script with target, verbose, and jobs arguments.",
    )

    # Target argument
    parser.add_argument(
        "-t", "--target", type=str, help="The target string to process.",
    )

    # Verbose flag
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging.",
    )

    # Jobs argument
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=None,
        help="Number of parallel processes to use (default: 1).",
    )

    args = parser.parse_args()
    cmd = ["ninja", "-Cbuild_cmake", args.target]
    if args.verbose:
        cmd.append("-v")
    if args.jobs is not None:
        cmd.extend(["-j", str(args.jobs)])
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    sys.exit(main())
