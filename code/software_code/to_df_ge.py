import pandas as pd
from os import getcwd
from io import StringIO
import numpy as np

fold_path = getcwd() + '/data/processed/tcga_ge_processed'
df = pd.read_csv(fold_path + '/0a4a9b5b-90d9-4789-af04-f931433808c1.rna_seq.augmented_star_gene_counts.tsv', delimiter='\t', skiprows=5)
df = df.set_axis(['gene_id', 'gene_name', 'gene_type', 'unstranded', 'stranded_first', 'stranded_second', 'tpm_unstranded', 'fpkm_unstranded', 'fpkm_uq_unstranded'], axis=1)
df.to_csv(getcwd() + '/data/processed/ge_full_df.csv', index=False)