#!/usr/bin/env python3
"""
Test runner for Detomo SQL AI

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py unit         # Run unit tests only
    python run_tests.py integration  # Run integration tests only
    python run_tests.py --verbose    # Run with verbose output
"""
import sys
import os
import subprocess
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def run_command(cmd):
    """Run command and return exit code"""
    print(f"Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main test runner"""
    # Parse arguments
    args = sys.argv[1:]
    verbose = "--verbose" in args or "-v" in args
    test_type = None

    for arg in args:
        if arg in ["unit", "integration", "all"]:
            test_type = arg
            break

    # Build pytest command
    base_cmd = ["pytest"]

    if verbose:
        base_cmd.append("-v")

    # Determine test path
    if test_type == "unit":
        print_header("Running Unit Tests")
        base_cmd.append("tests/unit/")
    elif test_type == "integration":
        print_header("Running Integration Tests")
        base_cmd.append("tests/integration/")
    else:
        print_header("Running All Tests")
        base_cmd.append("tests/")

    # Run tests
    exit_code = run_command(base_cmd)

    # Print summary
    print("\n" + "=" * 80)
    if exit_code == 0:
        print("  [PASS] All tests passed!")
    else:
        print(f"  [FAIL] Tests failed with exit code {exit_code}")
    print("=" * 80 + "\n")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
