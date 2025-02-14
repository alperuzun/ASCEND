import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score
import os
from os import getcwd
import requests
import io
import time

class ModelImplementation:
    def __init__(self, data_path, raw_results_path):
        self.data_path = data_path
        self.raw_results_path = raw_results_path

    def load_datasets(self):
        ge = pd.read_csv(f'{self.data_path}/ge_filtered.csv')
        cancer_target = ge['target']
        ge.drop(['target'], axis=1, inplace=True)

        meth = pd.read_csv(f'{self.data_path}/meth.csv')
        return ge, meth, cancer_target

    def create_keys(self):
        url = f"https://api.gdc.cancer.gov/data/839a4656-f2ce-4460-858a-8e6b314695ef"
        response = requests.get(url)
        # Decode and convert the content to a pandas DataFrame
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content), sep="\t", skiprows=1)
        gene_key = df[4:]['gene_id']

        url = f"https://api.gdc.cancer.gov/data/8e48755a-490f-45b4-b1bf-0fbf09485177"
        response = requests.get(url)

        # # Decode and convert the content to a pandas DataFrame
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content), sep="\t")
        df = df.set_axis(['cpg_island', f'patient_{i+1}'], axis=1)
        CpG_islands_key = df['cpg_island']

        return gene_key

    def ge_cancer_pred_model(self, ge, cancer_target):
        X_train, X_test, y_train, y_test = train_test_split(ge, cancer_target, train_size=0.7, random_state=1)

        clf = MLPClassifier(random_state=1, early_stopping=True, n_iter_no_change=5, max_iter=200, verbose=True)
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        print(f"Accuracy Score: {accuracy_score(y_test, preds):.2f}")

        coeffs = clf.coefs_[0]
        df_coeffs = pd.DataFrame(coeffs)
        mean_coeffs = df_coeffs.mean(axis=1)
        abs_mean_coeffs = mean_coeffs.abs()

        df = pd.DataFrame(abs_mean_coeffs.sort_values(ascending=False), columns=["Importance"])
        output_path = f'{self.raw_results_path}/abs_gene_coeffs.csv'
        df.to_csv(output_path, index=False)
        print(f"Gene coefficients saved to: {output_path}")
        return df

    def imp_CpG_identification(self, meth, ge_biomarkers, CpG_islands_key):
        imp_methyl_markers = {}
        for col in ge_biomarkers.columns:
            X_train, X_test, y_train, y_test = train_test_split(meth, ge_biomarkers[col], train_size=0.7, random_state=1)

            meth_clf = DecisionTreeRegressor()
            meth_clf.fit(X_train, y_train)
            coeffs = meth_clf.feature_importances_

            # Select top 5 features (or fewer if less than 5 exist)
            top_indices = coeffs.argsort()[-min(5, len(coeffs)):][::-1]
            imp_methyl_markers[col] = [
                (CpG_islands_key[i], coeffs[i]) for i in top_indices if i < len(CpG_islands_key)
            ]

        return imp_methyl_markers


# Main script execution
start = time.time()
if __name__ == "__main__":
    data_path = getcwd() + '/data/processed/combined_model_input_dfs'
    raw_results_path = getcwd() + '/test_results/pipeline_testing'

    # Ensure results directory exists
    os.makedirs(raw_results_path, exist_ok=True)

    # Initialize the model
    model = ModelImplementation(data_path, raw_results_path)

    # Step 1: Load keys
    gene_key = model.create_keys()

    # Step 2: Load datasets
    ge, meth, cancer_target = model.load_datasets()

    # Step 3: Perform gene prediction
    gene_coeffs = model.ge_cancer_pred_model(ge, cancer_target)

    # Step 4: Perform CpG identification
    imp_CpGs = model.imp_CpG_identification(meth, ge, CpG_islands_key)
    print("Important CpG sites identified:", imp_CpGs)
elapsed = time.time() - start
print(f'{elapsed//60} minutes, {elapsed-elapsed//60} seconds')
