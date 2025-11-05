#!/usr/bin/env python
"""
Verify installation and setup for STIR EARL Demo
"""

import sys
import subprocess
from pathlib import Path

def check_imports():
    """Check if required Python packages can be imported"""
    print("Checking Python packages...")
    packages = {
        'stir': 'STIR',
        'sirf_simind_connection': 'SIRF-SIMIND-Connection',
        'phantomgen': 'phantomgen',
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib',
        'scipy': 'SciPy',
    }

    missing = []
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT FOUND")
            missing.append(name)

    return missing

def check_simind():
    """Check if SIMIND is available"""
    print("\nChecking SIMIND...")
    try:
        result = subprocess.run(['which', 'simind'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            print(f"  ✓ SIMIND found at: {result.stdout.strip()}")
            return True
        else:
            print("  ✗ SIMIND not found in PATH")
            print("    Please install SIMIND and add it to your PATH")
            print("    Or update the notebook to point to your SIMIND installation")
            return False
    except Exception as e:
        print(f"  ✗ Error checking SIMIND: {e}")
        return False

def check_directories():
    """Check if required directories exist"""
    print("\nChecking directory structure...")
    required = [
        'par_files',
        'measured_data',
        'measured_data/tc99m',
        'measured_data/lu177',
    ]

    missing = []
    for dir_path in required:
        if Path(dir_path).exists():
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/ - NOT FOUND")
            missing.append(dir_path)

    return missing

def check_files():
    """Check if required files exist"""
    print("\nChecking required files...")
    required = [
        'stir_recon.ipynb',
        'stir_simind_utils.py',
        'Discovery670_tc99m.yaml',
        'Discovery670_lu177.yaml',
        'par_files/recon_OSEM.par',
    ]

    missing = []
    for file_path in required:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - NOT FOUND")
            missing.append(file_path)

    return missing

def main():
    print("="*60)
    print("STIR EARL Demo - Setup Verification")
    print("="*60)
    print()

    # Check Python packages
    missing_packages = check_imports()

    # Check SIMIND
    simind_ok = check_simind()

    # Check directories
    missing_dirs = check_directories()

    # Check files
    missing_files = check_files()

    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)

    all_ok = True

    if missing_packages:
        print(f"✗ Missing Python packages: {', '.join(missing_packages)}")
        print("  Install with: pip install -r requirements.txt")
        all_ok = False
    else:
        print("✓ All Python packages found")

    if not simind_ok:
        print("✗ SIMIND not available")
        print("  See SIMIND_macOS_setup.md for installation instructions")
        all_ok = False
    else:
        print("✓ SIMIND available")

    if missing_dirs:
        print(f"✗ Missing directories: {', '.join(missing_dirs)}")
        all_ok = False
    else:
        print("✓ All required directories found")

    if missing_files:
        print(f"✗ Missing files: {', '.join(missing_files)}")
        all_ok = False
    else:
        print("✓ All required files found")

    print()
    if all_ok:
        print("✓ Setup verification complete - ready to run!")
        print("\nTo start the demo:")
        print("  jupyter notebook stir_recon.ipynb")
        return 0
    else:
        print("✗ Setup incomplete - please fix the issues above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
