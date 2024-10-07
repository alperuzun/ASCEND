import pandas as pd
from os import getcwd
import requests
import json
import io

genes = pd.read_csv(getcwd() + '/data/processed/combined_model_input_dfs/ge_full_df.csv')
gene_names = genes['gene_name']

pseudogenes_file = getcwd() + '/data/pseudogenes.txt'
with open(pseudogenes_file, 'r') as file:
    pseudogenes = set(file.read().splitlines())

# Define filtering criteria
def filter_gene(gene):
    if (len(gene) < 1 or
        gene.startswith("LINC") or
        gene.startswith("LOC") or
        "orf" in gene or
        gene.startswith("RPS") or
        gene.startswith("RPL") or
        "Y_RNA" in gene or
        "-" in gene or
        "snoU" in gene or
        (any(char.isdigit() for char in gene) and len(gene) >= 10) or # Long sets of digits among MiRNA genes, for example: avoid inconsistencies
        gene.startswith("MIR") or
        gene.startswith("RNU") or
        gene.startswith("SNORD") or
        gene.startswith("SNORA") or
        gene.startswith("SCARNA") or
        gene.startswith("RNA45S") or
        gene.startswith("RNA28S") or
        gene.startswith("RNA18S") or
        gene.startswith("RNA5S") or
        gene in pseudogenes):
        # Add gene constraints as necessary
        return False
    return True

len_approved = 0
approved_dict = {}
for gene in gene_names:
    approved_gene_flag = filter_gene(gene)
    len_approved += approved_gene_flag
    approved_dict[gene] = approved_gene_flag
len_approved

approved_lst = []
for key, value in approved_dict.items():
    if value:
        approved_lst.append(key)
len(approved_lst)

filtered_df = df[df['gene_name'].isin(approved_lst)]


ge = pd.read_csv(getcwd() + '/data/processed/combined_model_input_dfs/ge.csv')
ge
approved_columns = []
gene_mapping = genes[['gene_id', 'gene_name']]
for i in range(0, len(gene_mapping)):
    if gene_mapping['gene_name'][i] in approved_lst:
        approved_columns.append(ge.columns[i])

len(approved_columns)
filtered_df = filtered_df[['gene_id', 'gene_name']]
filtered_df['approved_columns'] = approved_columns
filtered_df_unique = filtered_df.drop_duplicates(subset=['gene_name'])
len(filtered_df_unique)
filtered_df_unique.to_csv(getcwd() + '/data/processed/filtration/ge_mapping_key.csv', index=False)

ge_filtered = ge[list(filtered_df_unique['approved_columns'])]
ge_filtered['target'] = ge['target']

ge_filtered.to_csv(getcwd() + '/data/processed/combined_model_input_dfs/ge_filtered.csv', index=False)


# Create methods and materials: write out detailed steps and components
# Examples: Python version 3.8.3, modules ____, etc.
