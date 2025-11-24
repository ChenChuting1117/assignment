# Global Earthquake Data Visualization Project

An animated visualization project showcasing global earthquake data of magnitude 7 and above from 2012 to 2025.

I have created this visualisation of the geographical distribution of earthquakes using data on global earthquakes of magnitude 7 or above from 2012 to the present day.

There is a problem: I don't know why another window appears after closing my map window.

（Copilot helped me generate the following content, including the "requirements.txt". ）

## Project Files
- `earthquake.py` - Main visualization script
- `earthquake20122025.xlsx` - Earthquake data file
- `fonts/` - Font directory (contains Roboto_Condensed-Bold.ttf)
- `requirements.txt` - Python dependencies list

## Installation

1. Ensure Python 3.8 or higher is installed
2. Install required Python libraries:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pandas matplotlib cartopy numpy openpyxl setuptools_scm
```

## System Dependencies

### macOS
```bash
# If using Homebrew
brew install proj geos
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install libproj-dev proj-data proj-bin libgeos-dev
```

### Windows
Cartopy may require additional configuration on Windows. Using conda is recommended:
```bash
conda install -c conda-forge cartopy
```

## Running the Project

```bash
python earthquake.py
```

## Notes

1. Ensure the font file `fonts/Roboto_Condensed-Bold.ttf` exists
2. Ensure the earthquake data file `earthquake20122025.xlsx` exists
3. Cartopy will automatically download map data on first run, requiring internet connection
4. Animation may take some time to load and render

## Features

- Dynamic display of earthquake occurrence timeline
- Different colors and sizes of earthquake points based on magnitude
- Magnitude legend included
- Static distribution map of all earthquakes shown after animation ends