# SIMIND Setup for macOS (Apple Silicon)

This document describes the fixes required to run SIMIND on macOS with Apple Silicon (M1/M2/M3).

## Problem

SIMIND is distributed as x86_64 (Intel) binaries. When running on Apple Silicon Macs, several issues arise:
1. The binaries won't run without Rosetta 2 (Apple's x86_64 emulation layer)
2. macOS Gatekeeper blocks unsigned binaries downloaded from the internet
3. SIMIND requires the `SMC_DIR` environment variable to end with a trailing slash

## Solution Steps

### 1. Install Rosetta 2

Rosetta 2 allows Intel (x86_64) binaries to run on Apple Silicon Macs.

```bash
softwareupdate --install-rosetta --agree-to-license
```

**Note:** This is a one-time installation. Rosetta adds ~1-2GB to disk usage and introduces ~20-30% performance overhead, which is negligible for long-running SIMIND simulations.

### 2. Download Correct SIMIND Version

Download the **Mac Intel** version (e.g., `smc_mac_intel_64_current.tar.gz`), not the Linux version.

Extract to your desired location:
```bash
cd /path/to/your/project
tar -xzf ~/Downloads/smc_mac_intel_64_current.tar.gz
mv simind /path/to/your/project/simind
```

### 3. Remove Quarantine Flags

macOS marks downloaded files with a quarantine flag. Remove it from the entire SIMIND directory:

```bash
xattr -dr com.apple.quarantine /path/to/your/project/simind/
```

### 4. Ad-hoc Sign the Binaries

Since SIMIND binaries are unsigned, macOS may kill them with SIGKILL. Ad-hoc signing prevents this:

```bash
cd /path/to/your/project/simind
codesign -s - simind
codesign -s - bim
codesign -s - bis
codesign -s - change
codesign -s - simind_mpi
codesign -s - smc2castor
```

### 5. Fix SMC_DIR Environment Variable

SIMIND requires `SMC_DIR` to end with a trailing slash (`/`).

In your Python code or Jupyter notebook:
```python
import os
from pathlib import Path

simind_dir = Path('/path/to/your/project/simind')
os.environ['SMC_DIR'] = str(simind_dir / 'smc_dir') + '/'  # Note the trailing slash
os.environ['PATH'] = f"{simind_dir}:{os.environ.get('PATH', '')}"
```

**Important:** Without the trailing slash, SIMIND will fail with:
```
A final slash or backslash is needed to end the SMC_DIR environmental variable
```

## Verification

Test that SIMIND runs correctly:

```bash
export SMC_DIR=/path/to/your/project/simind/smc_dir/
export PATH=/path/to/your/project/simind:$PATH
simind
```

You should see SIMIND error messages about missing input files (expected), not "Bad CPU type" or being killed.

## OS-Agnostic Jupyter Notebook Setup

The notebook automatically detects the SIMIND installation:

```python
from pathlib import Path

notebook_dir = Path.cwd()
simind_dir = notebook_dir.parent / 'simind'
if not simind_dir.exists():
    simind_dir = notebook_dir.parent.parent / 'simind'

if simind_dir.exists():
    os.environ['SMC_DIR'] = str(simind_dir / 'smc_dir') + '/'
    os.environ['PATH'] = f"{simind_dir}:{os.environ.get('PATH', '')}"
```

This works on any OS (macOS, Linux, Windows with WSL) as long as SIMIND is installed relative to the notebook.

## Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Bad CPU type in executable` | Rosetta 2 not installed | Install Rosetta 2 (step 1) |
| `Command died with <Signals.SIGKILL: 9>` | Unsigned binary or quarantine flag | Remove quarantine and sign binaries (steps 3-4) |
| `A final slash or backslash is needed` | Missing trailing slash in `SMC_DIR` | Add `/` to end of `SMC_DIR` path (step 5) |
| macOS popup: "cannot verify developer" | Quarantine flag set | Remove quarantine flag (step 3) |

## Performance Notes

- Rosetta 2 adds ~20-30% overhead for x86_64 emulation
- For SIMIND simulations that take minutes to hours, this overhead is negligible
- The physics calculations dominate runtime, not the binary translation

## References

- SIMIND official website: https://www.simind.org/
- Apple Rosetta 2 documentation: https://support.apple.com/en-us/HT211861
