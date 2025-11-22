"""
miRNA Target Gene Analyzer - GUI Application

A simple graphical interface for analyzing miRNA target genes.
Matches miRNA predictions from miRDB with gene expression data.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import pandas as pd
import os
import sys
import threading
import requests
import gzip


class miRNAAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("miRNA Target Gene Analyzer")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variables
        self.mirna_file = tk.StringVar()
        self.gene_file = tk.StringVar()
        self.output_file = tk.StringVar(value="matching_genes.csv")
        self.mirna_column = tk.StringVar(value="systematic_name")
        self.gene_symbol_column = tk.StringVar(value="GeneSymbol")
        self.accession_column = tk.StringVar(value="GenbankAccession")
        self.is_running = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="miRNA Target Gene Analyzer", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # miRNA file selection
        ttk.Label(main_frame, text="miRNA File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.mirna_file, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Browse...", command=self.browse_mirna_file).grid(row=1, column=2, padx=5, pady=5)
        
        # Gene file selection
        ttk.Label(main_frame, text="Gene Expression File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.gene_file, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Browse...", command=self.browse_gene_file).grid(row=2, column=2, padx=5, pady=5)
        
        # Output file selection
        ttk.Label(main_frame, text="Output CSV File:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file, width=50).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Browse...", command=self.browse_output_file).grid(row=3, column=2, padx=5, pady=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        
        # Column configuration section
        config_label = ttk.Label(main_frame, text="Column Configuration (Optional)", font=('Arial', 10, 'bold'))
        config_label.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(5, 10))
        
        # miRNA column name
        ttk.Label(main_frame, text="miRNA Column Name:").grid(row=6, column=0, sticky=tk.W, pady=5, padx=(20, 0))
        mirna_col_entry = ttk.Entry(main_frame, textvariable=self.mirna_column, width=30)
        mirna_col_entry.grid(row=6, column=1, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text="(default: systematic_name)", font=('Arial', 8), foreground='gray').grid(row=6, column=2, sticky=tk.W, padx=5)
        
        # Gene symbol column name
        ttk.Label(main_frame, text="Gene Symbol Column:").grid(row=7, column=0, sticky=tk.W, pady=5, padx=(20, 0))
        gene_col_entry = ttk.Entry(main_frame, textvariable=self.gene_symbol_column, width=30)
        gene_col_entry.grid(row=7, column=1, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text="(default: GeneSymbol)", font=('Arial', 8), foreground='gray').grid(row=7, column=2, sticky=tk.W, padx=5)
        
        # Accession column name
        ttk.Label(main_frame, text="Accession Column:").grid(row=8, column=0, sticky=tk.W, pady=5, padx=(20, 0))
        acc_col_entry = ttk.Entry(main_frame, textvariable=self.accession_column, width=30)
        acc_col_entry.grid(row=8, column=1, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text="(default: GenbankAccession)", font=('Arial', 8), foreground='gray').grid(row=8, column=2, sticky=tk.W, padx=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        
        # Run button
        self.run_button = ttk.Button(main_frame, text="Run Analysis", command=self.run_analysis)
        self.run_button.grid(row=10, column=0, columnspan=3, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=11, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Log area
        ttk.Label(main_frame, text="Analysis Log:").grid(row=12, column=0, sticky=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=80, state='disabled')
        self.log_text.grid(row=13, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Configure text tags for colored output
        self.log_text.tag_config('success', foreground='green')
        self.log_text.tag_config('error', foreground='red')
        self.log_text.tag_config('info', foreground='blue')
        
        # Info label
        info_text = "This tool finds genes that are both predicted targets of your identified miRNAs\nand present in your gene expression data (using miRDB v6.0, score ≥ 80)."
        ttk.Label(main_frame, text=info_text, font=('Arial', 9), foreground='gray').grid(row=14, column=0, columnspan=3, pady=(10, 0))
        
        # Configure row weights for resizing
        main_frame.rowconfigure(13, weight=1)
    
    def browse_mirna_file(self):
        filename = filedialog.askopenfilename(
            title="Select miRNA File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            self.mirna_file.set(filename)
    
    def browse_gene_file(self):
        filename = filedialog.askopenfilename(
            title="Select Gene Expression File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            self.gene_file.set(filename)
    
    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save Output As",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
    
    def log(self, message, tag=None):
        """Add message to log area"""
        self.log_text.config(state='normal')
        if tag:
            self.log_text.insert(tk.END, message + '\n', tag)
        else:
            self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()
    
    def run_analysis(self):
        """Run the analysis in a separate thread"""
        if self.is_running:
            return
        
        # Validate inputs
        if not self.mirna_file.get():
            messagebox.showerror("Error", "Please select a miRNA file")
            return
        
        if not self.gene_file.get():
            messagebox.showerror("Error", "Please select a gene expression file")
            return
        
        if not self.output_file.get():
            messagebox.showerror("Error", "Please specify an output file")
            return
        
        # Clear log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Disable button and start progress
        self.run_button.config(state='disabled')
        self.progress.start(10)
        self.is_running = True
        
        # Run in separate thread
        thread = threading.Thread(target=self.perform_analysis)
        thread.daemon = True
        thread.start()
    
    def perform_analysis(self):
        """Perform the actual analysis"""
        try:
            self.log("=" * 70)
            self.log("Starting miRNA Target Gene Analysis", 'info')
            self.log("=" * 70)
            
            # Step 1: Extract miRNAs
            mirna_list = self.extract_mirna_from_file(
                self.mirna_file.get(), 
                self.mirna_column.get()
            )
            
            # Step 2: Extract genes and create accession mapping
            expression_genes, accession_to_gene = self.extract_genes_and_accessions(
                self.gene_file.get(),
                self.gene_symbol_column.get(),
                self.accession_column.get()
            )
            
            # Step 3: Get miRDB predictions
            mirna_targets_db = self.get_mirdb_predictions()
            
            if not mirna_targets_db:
                self.log("ERROR: Could not load miRDB predictions", 'error')
                return
            
            # Step 4: Process each miRNA
            results = []
            
            self.log("\n" + "=" * 70)
            self.log("Finding target genes for each miRNA...", 'info')
            self.log("=" * 70 + "\n")
            
            for mirna in mirna_list:
                self.log(f"Processing {mirna}...")
                
                # Skip non-standard miRNAs
                if mirna.startswith('dmr_'):
                    self.log("  → Skipping non-standard miRNA")
                    continue
                
                # Get target accessions from miRDB
                if mirna not in mirna_targets_db:
                    self.log("  → Not found in miRDB predictions")
                    continue
                
                target_accessions = mirna_targets_db[mirna]
                self.log(f"  Found {len(target_accessions)} predicted targets")
                
                # Convert accessions to gene symbols
                target_genes = []
                for accession in target_accessions:
                    if accession in accession_to_gene:
                        gene = accession_to_gene[accession]
                        if gene not in target_genes:
                            target_genes.append(gene)
                    else:
                        base_accession = accession.split('.')[0]
                        if base_accession in accession_to_gene:
                            gene = accession_to_gene[base_accession]
                            if gene not in target_genes:
                                target_genes.append(gene)
                
                if target_genes:
                    self.log(f"  Matched {len(target_genes)} to your gene data")
                
                # Find matches
                matching_genes = [gene for gene in target_genes if gene in expression_genes]
                
                for gene in matching_genes:
                    results.append({
                        'miRNA': mirna,
                        'Target_Gene': gene,
                        'Source': 'miRDB_v6.0_score>=80'
                    })
                
                if matching_genes:
                    self.log(f"  ✓ {len(matching_genes)} matches found", 'success')
                else:
                    self.log("  → No matches in expression data")
            
            # Step 5: Save results
            self.log("\n" + "=" * 70)
            self.log("Saving results...", 'info')
            self.log("=" * 70 + "\n")
            
            if results:
                df_results = pd.DataFrame(results)
                df_results.to_csv(self.output_file.get(), index=False)
                
                self.log(f"✓ Results saved to: {self.output_file.get()}", 'success')
                self.log(f"  Total matches: {len(results)}")
                self.log(f"  Unique miRNAs: {df_results['miRNA'].nunique()}")
                self.log(f"  Unique genes: {df_results['Target_Gene'].nunique()}")
                
                # Show summary
                self.log("\nTop miRNAs by target count:")
                summary = df_results.groupby('miRNA')['Target_Gene'].count().sort_values(ascending=False)
                for idx, (mirna, count) in enumerate(summary.head(5).items(), 1):
                    self.log(f"  {idx}. {mirna}: {count} genes")
                
                messagebox.showinfo("Success", f"Analysis complete!\n\n{len(results)} matching genes found.\n\nResults saved to:\n{self.output_file.get()}")
            else:
                self.log("⚠ No matching genes found", 'error')
                messagebox.showwarning("No Results", "No matching genes were found.\n\nThis may happen if:\n- Target genes don't overlap with your expression data\n- Accession formats don't match\n- Score threshold is too high")
            
            self.log("\n" + "=" * 70)
            self.log("Analysis complete!", 'success')
            self.log("=" * 70)
            
        except Exception as e:
            self.log(f"\nERROR: {str(e)}", 'error')
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")
        
        finally:
            # Re-enable button and stop progress
            self.progress.stop()
            self.run_button.config(state='normal')
            self.is_running = False
    
    def extract_mirna_from_file(self, mirna_file, mirna_column_name):
        """Extract miRNA symbols from file"""
        self.log(f"Reading miRNA file: {os.path.basename(mirna_file)}")
        self.log(f"  Looking for column: '{mirna_column_name}'")
        
        with open(mirna_file, 'r') as f:
            lines = f.readlines()
        
        header_idx = None
        for idx, line in enumerate(lines):
            if mirna_column_name in line:
                header_idx = idx
                break
        
        if header_idx is None:
            raise ValueError(f"Could not find '{mirna_column_name}' header in miRNA file.\n"
                           f"Please check the column name or use the default 'systematic_name'.")
        
        df = pd.read_csv(mirna_file, sep='\t', skiprows=header_idx)
        
        if mirna_column_name not in df.columns:
            raise ValueError(f"Column '{mirna_column_name}' not found in file.\n"
                           f"Available columns: {', '.join(df.columns.tolist())}")
        
        mirna_list = df[mirna_column_name].dropna().tolist()
        
        self.log(f"  Found {len(mirna_list)} miRNAs", 'success')
        return mirna_list
    
    def extract_genes_and_accessions(self, gene_file, gene_symbol_column, accession_column):
        """Extract genes and create accession mapping"""
        self.log(f"Reading gene expression file: {os.path.basename(gene_file)}")
        self.log(f"  Looking for columns: '{gene_symbol_column}' and '{accession_column}'")
        
        with open(gene_file, 'r') as f:
            lines = f.readlines()
        
        header_idx = None
        for idx, line in enumerate(lines):
            if gene_symbol_column in line:
                header_idx = idx
                break
        
        if header_idx is None:
            raise ValueError(f"Could not find '{gene_symbol_column}' header in gene file.\n"
                           f"Please check the column name or use the default 'GeneSymbol'.")
        
        df = pd.read_csv(gene_file, sep='\t', skiprows=header_idx)
        
        if gene_symbol_column not in df.columns:
            raise ValueError(f"Column '{gene_symbol_column}' not found in file.\n"
                           f"Available columns: {', '.join(df.columns.tolist())}")
        
        if accession_column not in df.columns:
            raise ValueError(f"Column '{accession_column}' not found in file.\n"
                           f"Available columns: {', '.join(df.columns.tolist())}")
        
        genes = set(df[gene_symbol_column].dropna().tolist())
        self.log(f"  Found {len(genes)} genes", 'success')
        
        # Create accession mapping
        accession_to_gene = {}
        for _, row in df.iterrows():
            if pd.notna(row.get(gene_symbol_column)) and pd.notna(row.get(accession_column)):
                accession = str(row[accession_column]).strip()
                gene = str(row[gene_symbol_column]).strip()
                accession_to_gene[accession] = gene
                base_accession = accession.split('.')[0]
                accession_to_gene[base_accession] = gene
        
        self.log(f"  Created accession mapping for {len(accession_to_gene)} entries", 'success')
        
        return genes, accession_to_gene
    
    def get_mirdb_predictions(self):
        """Download and load miRDB predictions (downloads on first run, then cached)"""
        # Determine cache file location
        if getattr(sys, 'frozen', False):
            # Running as exe - use user's AppData directory for cache
            cache_dir = os.path.join(os.environ.get('LOCALAPPDATA', '.'), 'miRNA_Analyzer')
        else:
            # Running as script - use current directory
            cache_dir = '.'
        
        # Create cache directory if it doesn't exist
        if cache_dir != '.' and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
        cache_file = os.path.join(cache_dir, 'mirdb_predictions.txt.gz')
        
        self.log("\nChecking miRDB predictions database...")
        
        # Check if we need to download
        if not os.path.exists(cache_file):
            self.log("  Database not found locally. Downloading from miRDB...", 'info')
            self.log("  This is a one-time download (~60 MB, may take a few minutes)", 'info')
            
            try:
                url = "https://mirdb.org/download/miRDB_v6.0_prediction_result.txt.gz"
                
                # Download with progress indication
                response = requests.get(url, stream=True, timeout=120)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(cache_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                percent = (downloaded / total_size) * 100
                                self.log(f"  Progress: {percent:.1f}% ({downloaded // (1024*1024)} MB / {total_size // (1024*1024)} MB)")
                
                self.log("  ✓ Download complete!", 'success')
                
            except Exception as e:
                self.log(f"  ERROR: Failed to download database: {e}", 'error')
                self.log("  Please check your internet connection and try again.", 'error')
                return None
        else:
            self.log(f"  ✓ Found cached database: {os.path.basename(cache_file)}", 'success')
        
        # Parse predictions directly from compressed file
        self.log("  Loading predictions from compressed file...")
        mirna_targets = {}
        
        try:
            with gzip.open(cache_file, 'rt', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 3:
                        mirna = parts[0]
                        target_accession = parts[1]
                        score = float(parts[2])
                        
                        if mirna.startswith('rno-') and score >= 80:
                            if mirna not in mirna_targets:
                                mirna_targets[mirna] = []
                            mirna_targets[mirna].append(target_accession)
            
            self.log(f"  ✓ Loaded {len(mirna_targets)} rat miRNAs with high-confidence predictions", 'success')
            return mirna_targets
            
        except Exception as e:
            self.log(f"  ERROR: Failed to parse database: {e}", 'error')
            # If parsing fails, delete the cache file so it will be re-downloaded
            if os.path.exists(cache_file):
                try:
                    os.remove(cache_file)
                    self.log("  Removed corrupted cache file. Please try running again.", 'info')
                except:
                    pass
            return None


def main():
    root = tk.Tk()
    app = miRNAAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
