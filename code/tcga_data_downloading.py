import os
import subprocess
from os import getcwd
import subprocess
import pandas as pd

# Path to gdc-client executable
gdc_client_path = getcwd() + '/data/manifests/gdc-client'

# Path to your manifest file
manifest_path = getcwd() + '/data/manifests/gdc_mirnaseq_manifest.txt'

def download_data(gdc_client_path, manifest_path, output_dir):
    command = [gdc_client_path, 'download', '-m', manifest_path, '-d', output_dir]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print the output in real-time
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    # Check for errors
    stderr = process.stderr.read()
    if stderr:
        print(stderr)

    # Ensure the process completed successfully
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)

# Output directory for downloaded files
output_dir = getcwd() + '/data/tcga_miRNAseq_data'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Download the data
download_data(gdc_client_path, manifest_path, output_dir)
