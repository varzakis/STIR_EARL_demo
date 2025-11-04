# STIR EARL Demo

Demonstration of SPECT simulation and reconstruction workflow for EARL (EANM Research Ltd.) accreditation using STIR, SIMIND, and custom Python tools.

## About

### EARL Standard
The EARL (EANM Research Ltd.) program provides guidelines and accreditation for quantitative PET/SPECT imaging. This demo uses the EARL NEMA IEC Body Phantom specification with 6 spheres to demonstrate a complete SPECT workflow including Monte Carlo simulation, scatter correction, and OSEM reconstruction.

### Key Packages

**phantomgen**: Python package for generating NEMA IEC Body phantoms with configurable sphere sizes, activities, and attenuation properties.

**SIRF-SIMIND-Connection**: Interface layer between STIR (reconstruction) and SIMIND (Monte Carlo simulation), enabling seamless data flow between simulation and reconstruction frameworks.

### What This Demo Shows

1. **Phantom Generation**: EARL NEMA phantom with 6 spheres (13-60mm diameter)
2. **SIMIND Simulation**: Monte Carlo SPECT simulation for Tc-99m or Lu-177
3. **Scatter Correction**:
   - DEW (Dual Energy Window) for Tc-99m
   - TEW (Triple Energy Window) for Lu-177
4. **OSEM Reconstruction**: STIR-based reconstruction with attenuation correction
5. **Comparison**: Measured vs simulated data analysis

## Installation

### Prerequisites

- **SIMIND** Monte Carlo simulator installed and in PATH (see [SIMIND_macOS_setup.md](SIMIND_macOS_setup.md) for macOS)
- **Conda** or Miniconda
- **Git**

### Setup

```bash
# Clone repositories
git clone <this-repo-url> STIR_EARL_demo
cd STIR_EARL_demo

# Clone dependencies (adjust paths as needed)
cd ..
git clone https://github.com/<org>/SIRF-SIMIND-Connection.git
git clone https://github.com/<org>/phantomgen.git
cd STIR_EARL_demo

# Create conda environment
conda env create -f environment.yml
conda activate stir-demo

# Install Python packages
pip install -r requirements.txt

# Verify setup
python verify_setup.py
```

## Usage

### Running the Demo

```bash
conda activate stir-demo
jupyter notebook stir_recon.ipynb
```

### Switching Between Isotopes

In the notebook, edit cell 1:

```python
ISOTOPE = "tc99m"  # Change to "lu177" for Lu-177
```

The notebook automatically configures:
- Energy windows (DEW for Tc-99m, TEW for Lu-177)
- Scanner parameters
- Phantom attenuation coefficients
- Scatter correction method

### Workflow Steps

1. **Configuration** - Choose isotope (tc99m or lu177)
2. **Phantom Generation** - Create NEMA phantom with spheres
3. **Simulation** - Run SIMIND Monte Carlo
4. **Scatter Correction** - Apply DEW or TEW
5. **Visualization** - Compare projections
6. **Reconstruction** - OSEM with attenuation correction
7. **Analysis** - Line profiles and quantitative metrics

## Repository Structure

```
├── stir_recon.ipynb              # Main demo notebook
├── stir_simind_utils.py          # Utility functions (DEW/TEW/OSEM)
├── Discovery670_tc99m.yaml       # Tc-99m scanner config
├── Discovery670_lu177.yaml       # Lu-177 scanner config
├── par_files/recon_OSEM.par     # STIR reconstruction parameters
├── measured_data/                # Real measured data for comparison
│   ├── tc99m/
│   └── lu177/
├── environment.yml               # Conda environment
├── requirements.txt              # Python dependencies
└── verify_setup.py              # Installation verification
```

## Troubleshooting

**SIMIND not found**: Ensure SIMIND is in your PATH or update the path in cell 1 of the notebook

**Import errors**: Check that SIRF-SIMIND-Connection and phantomgen are installed:
```bash
pip install -e ../SIRF-SIMIND-Connection
pip install -e ../phantomgen
```

**STIR errors**: Verify conda environment is activated: `conda activate stir-demo`

## Citation

If you use this demo, please cite:
- STIR: [reference]
- SIMIND: [reference]
- EARL: https://earl.eanm.org/

## License

See [LICENSE](LICENSE)
