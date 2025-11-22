# miRNA Target Gene Analyzer

A user-friendly tool for analyzing miRNA target genes by matching miRNA predictions from miRDB with gene expression data.

## Features

- **Simple GUI Interface**: Easy-to-use graphical interface for file selection
- **Automated Analysis**: Matches miRNA targets with gene expression data
- **miRDB Integration**: Uses miRDB v6.0 predictions (score ≥ 80)
- **CSV Output**: Results saved in easy-to-analyze CSV format

## Quick Start

### Option 1: Run with Batch File (Windows)

1. Double-click `Run_miRNA_Analyzer.bat`
2. The GUI will open automatically

### Option 2: Run with Python

```bash
python mirna_analyzer_gui.py
```

## Requirements

- Python 3.8 or higher
- Required packages (auto-installed):
  - pandas
  - requests

## How to Use

1. **Launch the application**
   - Use the batch file or run the Python script directly

2. **Select your input files**:
   - **miRNA File**: Your microarray results with identified miRNA (must have `systematic_name` column)
   - **Gene Expression File**: Your gene expression data (must have `GeneSymbol` and `GenbankAccession` columns)

3. **Choose output location**:
   - Specify where to save the results CSV file

4. **Run Analysis**:
   - Click "Run Analysis" button
   - The progress bar will show activity
   - Watch the log for detailed progress

5. **View Results**:
   - Results are saved to the specified CSV file
   - Contains three columns: `miRNA`, `Target_Gene`, `Source`

## Input File Format

### miRNA File (tab-separated .txt)
Must contain a column named `systematic_name` with miRNA identifiers:
```
systematic_name    p_value    Regulation    ...
rno-miR-124-5p    0.0044     down         ...
rno-miR-125b-5p   0.0316     down         ...
```

### Gene Expression File (tab-separated .txt)
Must contain columns `GeneSymbol` and `GenbankAccession`:
```
ProbeName    p_value    GeneSymbol    GenbankAccession    ...
A_42_P527070 0.0088     Gchfr         NM_133595          ...
A_44_P111123 0.0019     Mtus2         NM_001374100       ...
```

## Output Format

The results CSV contains matching genes:
```csv
miRNA,Target_Gene,Source
rno-miR-125b-5p,Sel1l,miRDB_v6.0_score>=80
rno-miR-125b-5p,Slc1a5,miRDB_v6.0_score>=80
rno-miR-126a-5p,Abcg5,miRDB_v6.0_score>=80
```

## miRDB Database

The application automatically downloads the miRDB v6.0 predictions database on first run:
- Downloads directly from miRDB (~60 MB compressed file)
- One-time download takes 2-5 minutes depending on connection speed
- Database is cached locally for future use
- Always uses the latest miRDB predictions
- Internet connection required only for first run

## Troubleshooting

### "Could not find systematic_name header"
- Ensure your miRNA file is tab-separated
- Check that the column is named exactly `systematic_name`

### "Could not find GeneSymbol header"
- Ensure your gene expression file is tab-separated
- Check for `GeneSymbol` and `GenbankAccession` columns

### "No matching genes found"
- This may happen if predicted targets don't overlap with your expression data
- Check that gene symbols in both files use the same format
- The score threshold (80) filters for high-confidence predictions only

## Technical Details

- **Database**: miRDB v6.0 (https://mirdb.org/)
- **Organism**: Rat (Rattus norvegicus)
- **Prediction Score**: ≥ 80 (high confidence)
- **Matching Method**: RefSeq accession-based gene symbol mapping

## Files Included

- `mirna_analyzer_gui.py` - Main GUI application
- `analyze_mirna_targets_optimized.py` - Command-line version (advanced users)
- `Run_miRNA_Analyzer.bat` - Windows launcher
- `README.md` - This file

## Support

For issues or questions:
1. Check that input files match the required format
2. Review the analysis log in the GUI for specific error messages
3. Ensure Python and required packages are installed

## Citation

If you use this tool in your research, please cite miRDB:
- Chen Y, Wang X. (2020) miRDB: an online database for prediction of functional microRNA targets. Nucleic Acids Research, 48:D127-D131.

---

**Version**: 1.0  
**Author**: Created for gene expression analysis
**License**: Free for academic and research use
