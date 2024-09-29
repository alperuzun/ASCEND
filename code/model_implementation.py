import requests
import time
import pandas as pd
from os import getcwd
import io
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, r2_score
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.inspection import permutation_importance
from sklearn.tree import DecisionTreeRegressor

ge = pd.read_csv(getcwd() + '/data/processed/combined_dfs/ge.csv')
ge

cancer_target = ge['target']
ge.drop(['target'], axis=1, inplace=True)

X_train, X_test, y_train, y_test = train_test_split(ge, cancer_target, train_size=0.7, random_state=1)

clf = MLPClassifier(random_state=1, max_iter=10)
clf = clf.fit(X_train, y_train)
preds = clf.predict(X_test)
accuracy_score(y_test, preds)

url = f"https://api.gdc.cancer.gov/data/839a4656-f2ce-4460-858a-8e6b314695ef"
response = requests.get(url)
# Decode and convert the content to a pandas DataFrame
content = response.content.decode('utf-8')
df = pd.read_csv(io.StringIO(content), sep="\t", skiprows=1)
gene_key = df[4:]['gene_id']


coeffs = clf.coefs_[0]
df_coeffs = pd.DataFrame(coeffs)
mean_coeffs = df_coeffs.mean(axis=1)
abs_mean_coeffs = mean_coeffs.abs()
df = pd.DataFrame(abs_mean_coeffs.sort_values(ascending=False))
df.to_csv(getcwd() + '/results/raw/abs_gene_coeffs.csv')

df1 = pd.read_csv(getcwd() + '/results/raw/abs_gene_coeffs.csv')

gene_key = gene_key.reset_index()['gene_id']
gene_ids = []
for idx in df1['Unnamed: 0']:
    gene_ids.append(gene_key[idx])
df1['gene_id'] = gene_ids
df1.to_csv(getcwd() + '/results/raw/abs_gene_coeffs_with_genes.csv')





meth = pd.read_csv(getcwd() + '/data/processed/combined_dfs/meth.csv').drop(['target'], axis=1)
ge_biomarkers = ge[['42182', '24875', '7216', '52254', '13927']]
ge_biomarkers

imp_methyl_markers = {}
for i in range(len(ge_biomarkers.columns)):
    X_train, X_test, y_train, y_test = train_test_split(meth, ge_biomarkers[ge_biomarkers.columns[i]], train_size=0.7, random_state=1)

    meth_clf = DecisionTreeRegressor()
    meth_clf = meth_clf.fit(X_train, y_train)
    preds = meth_clf.predict(X_test)
    meth_clf.score(X_test, y_test)
    coeffs = meth_clf.feature_importances_

    lst_coeffs = [coeff for coeff in coeffs]
    lst_coeffs1 = sorted(lst_coeffs, reverse=True)
    if len(lst_coeffs1) > 5:
        lst_coeffs1 = lst_coeffs1[0:5]
    imp_methyl_markers[ge_biomarkers.columns[i]] = lst_coeffs1

lst = []
for i in range(len(lst_coeffs)):
    if lst_coeffs[i] in lst_coeffs1:
        lst.append(i)
lst

uuid = '8e48755a-490f-45b4-b1bf-0fbf09485177'
url = f"https://api.gdc.cancer.gov/data/{uuid}"
response = requests.get(url)

# Decode and convert the content to a pandas DataFrame
content = response.content.decode('utf-8')
df = pd.read_csv(io.StringIO(content), sep="\t")  # Adjust separator if needed
df = df.set_axis(['cpg_island', f'patient_{i+1}'], axis=1)
CpG_islands_key = df['cpg_island']

lst
CpGs_lst = []
for idx in lst:
    CpGs_lst.append(CpG_islands_key[idx])
CpGs_lst
imp_methyl_markers
ge

del imp_methyl_markers ['42182']

df_methyl_markers = pd.DataFrame(imp_methyl_markers)

df_methyl_markers.to_csv(getcwd() + '/results/raw/biomarker_methyl_imp_scores.csv', index=False)

list(imp_methyl_markers.keys())
gene_key[42182], gene_key[24875], gene_key[7216], gene_key[52254], gene_key[13927]
meth
