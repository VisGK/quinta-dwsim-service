# DWSIM Installation Directory

This directory contains the DWSIM chemical process simulation software.

## Structure

```
dwsim/
├── DWSIM.exe          # Main DWSIM executable
├── Libraries/         # DWSIM libraries and dependencies
├── Examples/          # Example flowsheets and simulations
├── Documentation/     # DWSIM documentation
└── README.md         # This file
```

## Installation

The DWSIM software is automatically installed during the Docker build process using the `scripts/install_dwsim.sh` script.

## License

DWSIM is licensed under the GNU General Public License v3.0. See the main [LEGAL.md](../docs/LEGAL.md) file for complete license information.

## Usage

DWSIM is accessed through the REST API provided by this service. The service handles:

- Script execution
- File management
- Simulation monitoring
- Result processing

## Version

Current DWSIM version: 6.7.0

## Source

DWSIM is developed by Daniel Medeiros and contributors.
Original repository: https://github.com/DanWBR/dwsim6
