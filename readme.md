# Invoice Data Extraction from PDF Readme

## Introduction

This script allows you to extract invoice data from a PDF file and convert it into a JSON format. It can be useful when you have multiple invoices in PDF format and you need to organize them into a structured format for further analysis or processing.

## Requirements
Before running the script, ensure you have the following installed:

1. Python (version 3 or above)
2. pypdf library
3. Regular Expression library (re)
4. You can install pypdf and re libraries using pip:


```bash
pip install -r requirements.txt
```


## Usage
Download the Script: Save the provided Python script (invoice_extractor.py) to your local machine.


## Run the Script:

Open your terminal or command prompt.


Navigate to the directory where the script main.py is saved.

Give the name along with the path of the pdf from where data is to be extracted and also give name and path of ths json file where data has to be organized in tuples.

Run the script using the following command:

```bash
python main.py
```

Review Output: After running the script, it will create a file named data.json in the same directory. This JSON file contains the extracted invoice data in a structured format.


