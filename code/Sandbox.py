import requests
from os import getcwd
import pandas as pd
import time
import csv
from collections import Counter
import pickle
import os
import io
# # UUID to query
# uuid = 'e333c20d-ffbf-4e5d-a32e-3987898c0fd0'
# #
# # # GDC API endpoint
# url = f'https://api.gdc.cancer.gov/files/{uuid}'
# #
#
# params = {"fields": "cases.project.project_id", "expand": "cases.project"}
#
#
# # Make the request to the GDC API
# response = requests.get(url, params=params)
# data = response.json()
# project_id = data['data']['cases'][0]['project']['project_id']
# project_id

#
# uuid2 = '5419a015-093d-4328-bd55-cb33cce62243'
# url2 = f'https://api.gdc.cancer.gov/files/{uuid2}'
# response2 = requests.get(url2)
# data2 = response2.json()
# data2 = data2['data']
# data2['submitter_id']
#
# df = pd.read_csv(getcwd() + '/data/manifests/gdc_mirnaseq_manifest.txt', sep='\t')
# lst_ids = list(df['id'])
#
# patient_ids = []
# error_ids = []
# count = 1
# for uuid in lst_ids:
#     print(f'{100*round(count/len(lst_ids), 4)}% completed')
#     try:
#         url = f'https://api.gdc.cancer.gov/files/{uuid}'
#         response = requests.get(url)
#         data = response.json()
#         data = data['data']
#         patient_ids.append(data['submitter_id'])
#     except Exception as e:
#         print(f'Data unavailable for id: {uuid}')
#         error_ids.append(uuid)
#         pass
#     count += 1
# df.to_csv(getcwd() + '/data/patient_mapping/ge_patient_ids.csv', index=False)
# df = pd.Series(patient_ids)

def extract_uuids_from_manifest(manifest_file_path):
    uuids = []

    with open(manifest_file_path, 'r') as file:
        # Use DictReader to read the file assuming it's tab-delimited
        reader = csv.DictReader(file, delimiter='\t')

        # Extract UUIDs from the 'id' or 'file_id' column
        for row in reader:
            uuids.append(row['id'])

    return uuids


manifest_file_path = getcwd() + '/data/manifests/'


# Get the list of UUIDs
meth_uuid_list = extract_uuids_from_manifest(manifest_file_path + '/gdc_methylation_manifest.txt')
ge_uuid_list = extract_uuids_from_manifest(manifest_file_path + '/gdc_ge_manifest.txt')
miRNAseq_uuid_list = extract_uuids_from_manifest(manifest_file_path + '/gdc_mirnaseq_manifest.txt')

def get_case_id(uuid):
    ''' Describe function '''
    url = f"https://api.gdc.cancer.gov/files/{uuid}"
    response = requests.get(url)
    json_data = response.json()
    file_id = json_data['data']['file_id']

    url = f"https://api.gdc.cancer.gov/files/{file_id}?expand=cases"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        # Now we extract the case_id from the expanded cases data
        cases = json_data.get("data", {}).get("cases", [])
        if cases:
            case_id = cases[0].get("case_id", None)
            return case_id
        else:
            print(f"No cases found for File ID {file_id}")
            return None
    else:
        print(f"Error retrieving data for File ID {file_id}: {response.status_code}")
        return None

def execute_translation(mul, gul, miul, subset_size):
    start = time.time()
    meth_uuid_list = mul[0:subset_size]
    ge_uuid_list = gul[0:subset_size]
    miRNAseq_uuid_list = miul[0:subset_size]

    # Dictionary to store UUID to Case ID mapping
    meth_uuid_to_case_id = {}
    ge_uuid_to_case_id = {}
    miRNAseq_uuid_to_case_id = {}

    # Iterate through the list of UUIDs
    count = 0
    total_len = len(meth_uuid_list) + len(ge_uuid_list) + len(miRNAseq_uuid_list)
    try:
        for uuid in meth_uuid_list:
            count += 1
            case_id = get_case_id(uuid)
            meth_uuid_to_case_id[uuid] = case_id
            if count % 10 == 0:
                print( f'{100*round(count/ total_len, 4)}% completed' )
    except Exception as e:
        print(f'Error with iteration number: {count}')

    try:
        for uuid in ge_uuid_list:
            count += 1
            case_id = get_case_id(uuid)
            ge_uuid_to_case_id[uuid] = case_id
            if count % 10 == 0:
                print(f'{100 * round(count / total_len, 4)}% completed')
    except Exception as e:
        print(f'Error with iteration number: {count}')

    try:
        for uuid in miRNAseq_uuid_list:
            count += 1
            case_id = get_case_id(uuid)
            miRNAseq_uuid_to_case_id[uuid] = case_id
            if count % 10 == 0:
                print(f'{100 * round(count / total_len, 4)}% completed')
    except Exception as e:
        print(f'Error with iteration number: {count}')

    meth = list(meth_uuid_to_case_id.keys())
    ge = list(ge_uuid_to_case_id.values())
    mi = list(miRNAseq_uuid_to_case_id.values())

    stop = time.time()
    run_time = stop-start
    if run_time > 3600:
        print(f'{round(run_time/3600)} hours, {round((run_time%3600)/60)} min, {round(((run_time%3600)/60)%60)} sec')
    else:
        print(f'{round(run_time/60)} min, {round(run_time%60)} sec')

    if len(meth) + len(ge) + len(mi) == 300:
        print ("Passed initial check.")
    else:
        print ("ERROR: List lengths do not match subset_size.")

    return meth_uuid_to_case_id, ge_uuid_to_case_id, miRNAseq_uuid_to_case_id

meth_case_ids, ge_case_ids, mi_case_ids = execute_translation(meth_uuid_list, ge_uuid_list, miRNAseq_uuid_list, 1000)


ge_value_counts = Counter(ge_case_ids.values())

# Step 2: Find values that are duplicated (count > 1)
ge_duplicate_values = {value for value, count in ge_value_counts.items() if count > 1}

# Step 3: Create a new dictionary excluding the keys with duplicate values
filtered_ge_case_ids = {key: value for key, value in ge_case_ids.items() if value not in duplicate_values}


meth_value_counts = Counter(meth_case_ids.values())

# Step 2: Find values that are duplicated (count > 1)
duplicate_values = {value for value, count in meth_value_counts.items() if count > 1}

# Step 3: Create a new dictionary excluding the keys with duplicate values
filtered_meth_case_ids = {key: value for key, value in meth_case_ids.items() if value not in duplicate_values}

meth_patients = list(filtered_meth_case_ids.values())
ge_patients = list(filtered_ge_case_ids.values())
# mi_patients = list(mi_case_ids.values())
len(ge_patients), len(meth_patients)


meth_ge_ps = set(meth_patients) & set(ge_patients)
meth_overlap_uuids = [uuid for uuid, patient_id in meth_case_ids.items() if patient_id in meth_ge_ps]
ge_overlap_uuids = [uuid for uuid, patient_id in ge_case_ids.items() if patient_id in meth_ge_ps]
len(meth_overlap_uuids), len(ge_overlap_uuids), len(meth_ge_ps)


# meth_mi_ps = [x for x in meth_patients if x in mi_patients]
# mi_overlap_uuids = [key for key, value in meth_case_ids.items() if value in meth_mi_ps]
# meth_mi_uuids
#

def get_cancer_type_from_uuid(uuids):
    start = time.time()
    project_ids = {}
    count = 0
    for uuid in uuids:
        count += 1
        url = f"https://api.gdc.cancer.gov/files/{uuid}"

        # Parameters to retrieve only the required fields
        params = {
            "fields": "cases.project.project_id",
            "expand": "cases.project"
        }

        # Make the request to the GDC API
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Extract the project_id which corresponds to the cancer type
            project_id = data['data']['cases'][0]['project']['project_id']
            project_ids[uuid] = project_id

        if count % 6 == 0:
            print(f'{100 * round(count / len(uuids), 4)}% completed')

    stop = time.time()
    run_time = stop - start
    if run_time > 3600:
        print(f'{round(run_time/3600)} hours, {round((run_time%3600)/60)} min, {round(((run_time%3600)/60)%60)} sec')
    else:
        print(f'{round(run_time/60)} min, {round(run_time%60)} sec')

    return project_ids

ge_cancer_type = get_cancer_type_from_uuid(ge_overlap_uuids)
meth_cancer_type = get_cancer_type_from_uuid(meth_overlap_uuids)
# mi_cancer_type = get_cancer_type_from_uuid(mi_overlap_uuids)

types = list(ge_cancer_type.values())
count_dict = dict(Counter(types))
sorted_type_count_dict = dict(sorted(count_dict.items(), key=lambda item: item[1], reverse=True))
sorted_type_count_dict

meth_types = list(meth_cancer_type.values())
meth_count_dict = dict(Counter(meth_types))
meth_sorted_type_count_dict = dict(sorted(meth_count_dict.items(), key=lambda item: item[1], reverse=True))
meth_sorted_type_count_dict
# types = list(mi_cancer_type.values())
# count_dict = dict(Counter(types))
# sorted_type_count_dict1 = dict(sorted(count_dict.items(), key=lambda item: item[1], reverse=True))
# sorted_type_count_dict1


ge_file = open(getcwd() + '/data/processed/cancer_type_files/ge_cancer_types', 'wb')
# mi_file = open(getcwd() + '/data/processed/cancer_type_files/mi_cancer_types', 'wb')
pickle.dump(ge_cancer_type, ge_file)
# pickle.dump(mi_cancer_type, mi_file)
ge_file.close()
# mi_file.close()

meth_file = open(getcwd() + '/data/processed/cancer_type_files/meth_cancer_types', 'wb')
pickle.dump(meth_cancer_type, meth_file)
meth_file.close()

def filter_by_cancer_type(target_cancer_id, cancer_type_list):
    target_uuid_list = []
    for uuid, cancer in cancer_type_list.items():
        if cancer == target_cancer_id:
            target_uuid_list.append(uuid)
    print(f"Number of {target_cancer_id} patients in dataset: {len(target_uuid_list)}")
    return target_uuid_list

BRCA_uuids_ge = filter_by_cancer_type('TCGA-BRCA', ge_cancer_type)
BRCA_uuids_meth = filter_by_cancer_type('TCGA-BRCA', meth_cancer_type)

# BRCA_uuids_mi = filter_by_cancer_type('TCGA-BRCA', mi_cancer_type)
# BRCA_uuids_ge

# GDC API endpoint for file metadata
GDC_API_ENDPOINT = "https://api.gdc.cancer.gov/files/"

def get_sample_type(uuid):
    """
    Given a UUID, this function checks whether the associated data is cancerous or non-cancerous.
    """
    # Define parameters for the API call
    params = {
        "fields": "cases.samples.sample_type,cases.samples.portions.analytes.aliquots.submitter_id",  # Metadata fields
        "expand": "cases.samples.portions.analytes.aliquots",  # To expand aliquot details
        "pretty": "true"  # For better formatting of the output (optional)
    }

    # Make the request to the GDC API
    response = requests.get(GDC_API_ENDPOINT + uuid, params=params)

    if response.status_code == 200:
        data = response.json()

        # Extract sample type and submitter ID from the response
        try:
            sample_type = data['data']['cases'][0]['samples'][0]['sample_type']
            submitter_id = data['data']['cases'][0]['samples'][0]['portions'][0]['analytes'][0]['aliquots'][0]['submitter_id']
        except (KeyError, IndexError) as e:
            return f"Error parsing metadata for UUID {uuid}: {e}"
    else:
        return f"Failed to fetch data for UUID {uuid}. Status code: {response.status_code}"
    return sample_type


def iterate_sample_types(uuids):
    start = time.time()
    sample_type_dict = {}
    count = 0
    for uuid in uuids:
        sample_type = get_sample_type(uuid)
        if "Tumor" in sample_type:
            sample_type_dict[uuid] = 'Cancerous'
        elif "Normal" in sample_type:
            sample_type_dict[uuid] = 'Non-Cancerous'
        else:
            sample_type_dict[uuid] = 'Unclassified'
        count += 1
        if count % 5 == 0:
            print(f'{100 * round(count / len(uuids), 4)}% completed')
    run_time = time.time()-start
    print(f'{round(run_time/60)} min, {round(run_time%60)} sec')
    return sample_type_dict

ge_cancerous_dict = iterate_sample_types(BRCA_uuids_ge)
meth_cancerous_dict = iterate_sample_types(BRCA_uuids_meth)



ge_target = []
for tar in ge_cancerous_dict.values():
    if tar == 'Cancerous':
        ge_target.append(1)
    else:
        ge_target.append(0)

meth_target = []
for tar in meth_cancerous_dict.values():
    if tar == 'Cancerous':
        meth_target.append(1)
    else:
        meth_target.append(0)


meth_dfs = {}
# Iterate over the list of UUIDs
for i, uuid in enumerate(BRCA_uuids_meth):
    url = f"https://api.gdc.cancer.gov/data/{uuid}"
    response = requests.get(url)

    if response.status_code == 200:
        # Decode and convert the content to a pandas DataFrame
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content), sep="\t")  # Adjust separator if needed
        df = df.set_axis(['cpg_island', f'patient_{i+1}'], axis=1)  # Label columns per patient
        # Store the DataFrame in the dictionary
        meth_dfs[f'patient_{i+1}'] = df[f'patient_{i+1}']
    else:
        print(f"Failed to download file for UUID {uuid}. Status code: {response.status_code}")

    if i % 5 == 0:
        print(f'{100 * round(i / len(BRCA_uuids_meth), 4)}% completed')


meth_comb_df = pd.concat(meth_dfs.values(), axis=1, join='inner')
meth_comb_df = meth_comb_df.transpose()
meth_comb_df['target'] = meth_target[0:101]
meth_comb_df.to_csv(getcwd() + '/data/processed/combined_dfs/meth.csv', index=False)


ge_dfs = {}
for x, uuid in enumerate(BRCA_uuids_ge):
    url = f"https://api.gdc.cancer.gov/data/{uuid}"
    response = requests.get(url)
    if response.status_code == 200:
        # Decode and convert the content to a pandas DataFrame
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content), sep="\t", skiprows=1)
        df = df[4:]
        # Store the DataFrame in the dictionary
        ge_dfs[f'patient_{x+1}'] = df['tpm_unstranded']
    else:
        print(f"Failed to download file for UUID {uuid}. Status code: {response.status_code}")

    if x % 5 == 0:
        print(f'{100 * round(x / len(BRCA_uuids_ge), 4)}% completed')

len(ge_dfs)
ge_comb_df = pd.concat(ge_dfs.values(), axis=1, join='inner')
ge_comb_df = ge_comb_df.transpose()[0:101]
ge_comb_df['target'] = ge_target[0:101]
ge_comb_df.to_csv(getcwd() + '/data/processed/combined_dfs/ge.csv', index=False)
