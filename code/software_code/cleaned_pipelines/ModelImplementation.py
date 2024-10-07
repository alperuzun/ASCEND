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

class ModelImplementation:
    def __init__(self, data_path, raw_results_path):
        self.data_path = data_path
        self.raw_results_path = raw_results_path

    def create_keys():
        url = f"https://api.gdc.cancer.gov/data/839a4656-f2ce-4460-858a-8e6b314695ef"
        response = requests.get(url)
        # Decode and convert the content to a pandas DataFrame
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content), sep="\t", skiprows=1)
        gene_key = df[4:]['gene_id']


        url = f"https://api.gdc.cancer.gov/data/8e48755a-490f-45b4-b1bf-0fbf09485177"
        response = requests.get(url)

        # Decode and convert the content to a pandas DataFrame
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content), sep="\t")  # Adjust separator if needed
        df = df.set_axis(['cpg_island', f'patient_{i+1}'], axis=1)
        CpG_islands_key = df['cpg_island']

        return gene_key, CpG_islands_key

    gene_key, CpG_islands_key = create_keys()

    def load_datasets(data_path):
        ge = pd.read_csv(f'{data_path}/ge.csv')
        cancer_target = ge['target']
        ge.drop(['target'], axis=1, inplace=True)

        meth = pd.read_csv(f'{data_path}/meth.csv'), axis=1)

        return ge, meth, cancer_target

    ge, meth, cancer_target = load_datasets(data_path)

    def ge_cancer_pred_model(raw_results_path):
        X_train, X_test, y_train, y_test = train_test_split(ge, cancer_target, train_size=0.7, random_state=1)

        clf = MLPClassifier(random_state=1, max_iter=10)
        clf = clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        print(accuracy_score(y_test, preds))

        coeffs = clf.coefs_[0]
        df_coeffs = pd.DataFrame(coeffs)
        mean_coeffs = df_coeffs.mean(axis=1)
        abs_mean_coeffs = mean_coeffs.abs()

        df = pd.DataFrame(abs_mean_coeffs.sort_values(ascending=False))
        df.to_csv(f'{raw_results_path}/abs_gene_coeffs.csv')
        return df

    df = ge_cancer_pred_model(raw_results_path)

    def imp_CpG_identification(ge_biomarkers):
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

        CpGs_lst = []
        for idx in lst:
            CpGs_lst.append(CpG_islands_key[idx])

        return CpGs_lst, imp_methyl_markers
