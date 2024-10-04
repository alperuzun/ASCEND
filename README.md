# ASCEND

In molecular biology, gene expression serves as a crucial indicator of cellular function and health. Alterations in these expression patterns, often influenced by epigenetic changes such as DNA methylation, can signify the presence of various diseases, including cancer. As our understanding of these complex biological processes deepens, the need for sophisticated analytical tools becomes increasingly apparent.

ASCEND is a novel approach to cancer analysis that integrates transcriptomics and epigenetics. By simultaneously examining gene expression and DNA methylation data, ASCEND provides a comprehensive view of the molecular landscape in cancer. This dual-analysis strategy aims to enhance cancer prediction capabilities and identify potential biomarkers and therapeutic targets, potentially contributing to the development of more effective and personalized treatment strategies.

The ASCEND software employs machine learning techniques to analyze genomic data. It utilizes a Multilayer Perceptron Classifier to identify patterns that distinguish healthy individuals from those with cancer. This analysis yields a set of genes that serve as potential biomarkers, offering insights into the underlying mechanisms of the disease. The methylation analysis module of ASCEND uses linear regression to explore the relationship between gene expression and DNA methylation patterns. This integrated approach provides a more nuanced understanding of how epigenetic changes may influence gene activity in cancer development.

The potential utility of ASCEND extends beyond its analytical capabilities. By identifying key biomarker genes and their associated methylation sites, ASCEND may open new avenues for early detection and intervention in cancer research. These insights could potentially be used to develop more sensitive diagnostic tools, aiming to detect cancers at earlier, more treatable stages. Furthermore, the identification of specific methylation patterns associated with cancer progression could inform the development of epigenetic therapies, targeting the mechanisms of gene dysregulation in cancer cells.

While the initial focus of ASCEND is on Breast Adenocarcinoma, its architecture allows for potential application across various cancer types. This scalability ensures that as our understanding of different cancers grows, ASCEND can be adapted to provide insights across the oncological spectrum. The software's capacity to process and analyze large datasets also makes it a potentially valuable tool in the era of big data, where the volume of genomic information continues to expand.

Future development plans for ASCEND include enhancing its accessibility and user experience. The proposed development of a graphical user interface aims to allow researchers to interact with the software more intuitively, adjusting parameters and visualizing results. This interface could potentially make ASCEND more user-friendly and promote transparency in cancer analytics, allowing researchers to better understand and interpret the complex relationships between genes, methylation patterns, and cancer development.

In conclusion, ASCEND represents a new approach in cancer research, integrating transcriptomic and epigenetic analysis to offer a more comprehensive picture of the molecular basis of cancer. As research in cancer biology progresses, tools like ASCEND may play a role in translating genetic insights into clinical applications, potentially contributing to the development of prevention strategies and targeted therapies for cancer patients.


# Installation
ASCEND has not yet been incorporated into a front-end user interface to be used. Thus, the software can be run by utilizing the code from this repository. In the near future, however, ASCEND's GUI will be incorporated into a GUI that can be installed and used as a web application.

# Getting Started
### Running the Software
Once this repository has been downloaded to your local machine, navigate to the AtomIDE or your preferred IDE of choice. Ensure that Python has been installed. Navigate to the code folder and then, the cleaned_pipelines folder. In this folder, the subprocesses of the ASCEND software have been broken down for you to run.

### Input Data
In order to run the model, you will need gene expression data in the format of a csv file. If this data is from the TCGA database, then


# Authors
This project was developed by Jay Ananth and Dr. Alper Uzun in the Uzun Lab at Brown University.


# Contact
Reach out to alper_uzun@brown.edu with any questions.
