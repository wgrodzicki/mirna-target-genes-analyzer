# miRNA Target Gene Analyzer

A user-friendly tool for analyzing miRNA target genes by matching miRNA predictions from miRDB with gene expression data.

## Features

- **Simple GUI Interface**: Easy-to-use graphical interface for file selection
- **Two Analysis Modes**: With or without gene expression data comparison
- **Automated Analysis**: Matches miRNA targets with gene expression data (optional)
- **miRDB Integration**: Uses miRDB v6.0 predictions (score ≥ 80)
- **Flexible Output Formats**: Choose between CSV or TXT table format
- **Auto-Download Database**: Downloads latest miRDB data on first run

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
   - **miRNA File** (required): Your microarray results with identified miRNA (must have `systematic_name` column)
   - **Gene Expression File** (optional): Your gene expression data (must have `GeneSymbol` and `GenbankAccession` columns)
     - **With this file**: Finds targets that match your expression data
     - **Without this file**: Returns all predicted targets from miRDB

3. **Select output format**:
   - Choose between CSV (comma-separated) or TXT (tab-delimited table)

4. **Choose output location**:
   - Specify where to save the results file

5. **Run Analysis**:
   - Click "Run Analysis" button
   - The progress bar will show activity
   - Watch the log for detailed progress

6. **View Results**:
   - Results are saved to the specified file
   - CSV: Two columns (`miRNA`, `Target_Gene`)
   - TXT: Table format with miRNAs as columns

## Analysis Modes

### Mode 1: With Gene Expression File
Finds the intersection between miRDB predicted targets and your gene expression data.
- **Use case**: You have expression data and want to know which predicted targets are present in your dataset
- **Output**: Gene symbols that are both predicted targets and in your expression data

### Mode 2: Without Gene Expression File
Returns all high-confidence predicted targets from miRDB.
- **Use case**: You want a complete list of predicted targets without filtering
- **Output**: Target accessions directly from miRDB database
- **Advantage**: Get all predictions even if you don't have expression data

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

### CSV Format (Comma-separated)
Results contain matching genes with two columns:
```csv
miRNA,Target_Gene
rno-miR-125b-5p,Sel1l
rno-miR-125b-5p,Slc1a5
rno-miR-126a-5p,Abcg5
```

### TXT Format (Tab-delimited Table)
Results formatted as a table with miRNAs as column headers:
```
rno-miR-125b-5p	rno-miR-126a-5p	rno-miR-1b
Sel1l	Abcg5	Bsn
Slc1a5	Rtn4rl1	Myo1e
Tmem120b	Ppp1r10	Atp6v1a
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
- Or leave the gene expression file blank to get all predicted targets

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
**Author**: Wojciech Grodzicki  
**License**: Free for academic and research use

Built with an AI agent.