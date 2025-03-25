#!/usr/bin/env python3
import os
import subprocess
import sys


def check_python_version():
    required_version = (3, 8)
    current_version = sys.version_info[:2]

    if current_version < required_version:
        print(
            "Error: Python "
            f"{required_version[0]}.{required_version[1]} or higher is required"
        )
        return False
    return True


def check_uv_installation():
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error: uv is not properly installed")
            return False
        print(f"uv version: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("Error: uv is not installed")
        return False


def check_dependencies():
    try:
        # Check if pre-commit is installed
        pre_commit_result = subprocess.run(
            ["pre-commit", "--version"], capture_output=True, text=True
        )
        if pre_commit_result.returncode != 0:
            print("Error: pre-commit is not properly installed")
            return False
        print(f"pre-commit version: {pre_commit_result.stdout.strip()}")

        # Check if pre-commit hook file exists and is properly configured
        hook_path = os.path.join(".git", "hooks", "pre-commit")
        if not os.path.exists(hook_path):
            print("Error: pre-commit hook file is missing")
            return False

        with open(hook_path) as f:
            hook_content = f.read()
            if "pre-commit.com" not in hook_content:
                print("Error: pre-commit hook file is not properly configured")
                return False

        # Check if virtual environment exists
        venv_result = subprocess.run(
            ["uv", "venv", "list"], capture_output=True, text=True
        )
        if venv_result.returncode != 0:
            print("Warning: No virtual environment found")
            return False

        # Check if required packages are installed
        required_packages = [
            "pre-commit",
            "black",
            "flake8",
            "mypy",
            "types-setuptools",
        ]
        for package in required_packages:
            result = subprocess.run(
                ["uv", "pip", "show", package], capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Error: {package} is not installed")
                return False

        print("All dependencies and pre-commit hooks are properly configured")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to verify dependencies: {str(e)}")
        return False


def main():
    checks = [
        ("Python version", check_python_version),
        ("uv installation", check_uv_installation),
        ("Dependencies", check_dependencies),
    ]

    all_passed = True
    print("Running environment validation checks...")
    print("-" * 40)

    for name, check in checks:
        print(f"\nChecking {name}...")
        if not check():
            all_passed = False

    print("\n" + "-" * 40)
    if all_passed:
        print("✅ All checks passed!")
        sys.exit(0)
    else:
        print("❌ Some checks failed. Please fix the issues before committing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
