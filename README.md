# CV CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![PyPI version](https://badge.fury.io/py/cv-cli.svg)](https://pypi.org/project/cv-cli/) [![GitHub last commit](https://img.shields.io/github/last-commit/danielaca18/cv-cli.svg)](https://github.com/danielaca18/cv-cli/commits/main)

CV CLI is a simple Python script that generates a LaTeX resume using the Jinja2 templating engine. It allows you to create a professional-looking resume in PDF format with minimal effort.

## Features
- Easy to use: Just fill in a YAML file with your information and run the script.
- Multiple Profiles: Supports multiple profiles, allowing you to create different resumes for different job types.
- Customizable: Supports multiple templates and allows you to create your own.
- Output in PDF format: Generates a high-quality PDF resume using LaTeX.
- Cross-platform: Works on Windows, macOS, and Linux.

## Resume Previews
| Default Template | Sheets Template |
|------------------|-----------------|
| ![Default Template](https://github.com/Danielaca18/cv-cli/blob/main/previews/default.png?raw=true) | ![Sheets Template](https://github.com/Danielaca18/cv-cli/blob/main/previews/sheets.png?raw=true) |


## Getting Started
### Prerequisites
- Python 3.6 or higher
- LaTeX distribution (e.g., TeX Live, MikTeX) installed on your system

### Installation
```bash
   pip install cv-cli
```

## Usage
```bash
cv-cli <COMMAND> [OPTIONS]  
```
Ex. ```cv-cli build -p example -t default```
## Commands
##### Build

  Build CV PDF.
```bash
build [OPTIONS]
```
##### Profiles
  Create, edit and sync Profiles.
   ```bash
  cv-cli profiles new <name>
  cv-cli profiles edit <name>
  cv-cli profiles clone <url>
  cv-cli profiles init
  cv-cli profiles rm <name>
  ```

##### Templates
  Create, edit and sync Templates:  
  ```bash
  cv-cli templates new <name>
  cv-cli templates edit <name>
  cv-cli templates clone <url>
  cv-cli templates init
  cv-cli templates rm <name>
  ```

## Acknowledgements
- This project uses the [Resume Template](https://github.com/jakegut/resume) by Jake Gutierrez as a base for the LaTeX templates. Thank you for your work!
- The provided sheets template is inspired by the famous [Sheets Resume](https://sheetsresume.com/resume-template/) by Sheets Resume.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Planned Features
- Git Integration
    - Import & Sync Profiles
    - Import & Sync Templates
- Template Configuration
    - Name templates
- Editor Integration
    - VSCode
- Verbosity Argument
