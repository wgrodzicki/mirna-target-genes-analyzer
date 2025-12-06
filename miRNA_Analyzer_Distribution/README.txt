# miRNA Target Gene Analyzer - Distribution Package

## What's Included

This package contains:

1. **miRNA_Analyzer.exe** - Standalone executable (no Python required!)
2. **README.md** - User guide and documentation
3. **Sample files** - Example input files for testing

## Quick Start (Executable Version)

1. **Run the Application**
   - Simply double-click `miRNA_Analyzer.exe`
   - No Python installation needed!
   - Windows may show a security warning on first run - click "More info" → "Run anyway"

2. **Select Your Files**
   - Browse for your miRNA file (File #1)
   - Browse for your gene expression file (File #2)
   - Choose output format (CSV or TXT)
   - Choose where to save the results

3. **Run Analysis**
   - Click "Run Analysis"
   - Wait for completion (first run downloads database ~100MB)
   - Results saved as CSV file

## System Requirements

- Windows 10 or later (64-bit)
- 100 MB free disk space (for database cache)
- Internet connection (first run only to download database)

## Input File Requirements

### miRNA File (Required)
- Format: Tab-separated text (.txt)
- Default column: `systematic_name` (configurable in GUI)
- Example: `file-#1-mirna.txt`

### Gene Expression File (Optional)
- Format: Tab-separated text (.txt)
- Default columns: `GeneSymbol`, `GenbankAccession` (configurable in GUI)
- Example: `file-#2-genes.txt`
- **Leave blank** to get all predicted targets from miRDB without filtering

### Custom Column Names
- The application provides optional fields to configure column names
- If your files use different column headers, enter them in the "Column Configuration" section
- Default values are pre-filled and work with the sample files

## Analysis Modes

The tool offers two ways to analyze your miRNAs:

### With Gene Expression File
- Matches miRDB predictions against your expression data
- Returns only genes that are both predicted targets AND in your dataset
- Best for: Finding which predicted targets are present in your experiment

### Without Gene Expression File
- Returns ALL predicted targets from miRDB for your miRNAs
- No filtering - complete list of high-confidence predictions
- Best for: Exploring all possible targets without expression data constraints

## Output

### CSV Format
Comma-separated file with two columns:
- `miRNA` - The miRNA identifier
- `Target_Gene` - Matching gene symbol

### TXT Format
Tab-delimited table:
- Column headers are miRNA identifiers
- Rows below each column contain target genes for that miRNA
- Easy to view side-by-side comparison

## Database Information

The miRDB prediction database is downloaded automatically:
- Downloads on first run from miRDB.org (~60 MB)
- Takes 2-5 minutes depending on internet speed
- miRDB v6.0 with high-confidence predictions (score ≥ 80)
- Cached locally - subsequent runs work offline
- Always uses the latest miRDB predictions

## Troubleshooting

### Windows Security Warning
Windows Defender may flag the executable as "unrecognized"
- This is normal for new executables
- Click "More info" → "Run anyway"
- Or right-click → Properties → Check "Unblock"

### "Cannot find file" errors
- Ensure input files are tab-separated
- Check column names match requirements
- Use the sample files to test first

### No matches found
- Predicted targets may not overlap with your data
- Try with sample files to verify the tool works
- Check that gene symbols are in standard format

## Alternative: Python Version

If you prefer to run with Python:
1. Install Python 3.8+
2. Install packages: `pip install pandas requests`
3. Run: `python mirna_analyzer_gui.py`

## Distribution

To share this tool:
1. Copy the entire folder
2. Recipients can run `miRNA_Analyzer.exe` directly
3. No installation or setup required

## Support

For questions or issues:
- Check the log window in the application
- Review README.md for detailed documentation
- Verify input file format matches requirements

## Citation

miRDB database:
Chen Y, Wang X. (2020) miRDB: an online database for prediction of functional microRNA targets. Nucleic Acids Research, 48:D127-D131.

---

**Version**: 1.0
**Build Date**: November 2025
**Platform**: Windows 64-bit
