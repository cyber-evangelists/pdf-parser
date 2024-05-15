import re
from PyPDF2 import PdfReader
import json

def extract_data_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PdfReader(file)
        report_date = None
        data_tuples = []

        for page in reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
             
                if "Invoice Report by Contractor" in line:
                    report_date_match = re.search(r'(\d{2}/\d{2}/\d{4})$', line)
                    if report_date_match:
                        report_date = report_date_match.group(1)
                
             
                if "Assigned Owner" in line:
                    assigned_owner_match = re.search(r'Assigned Owner (A\d+\s+.+)$', line)
                    if assigned_owner_match:
                        assigned_owner=(assigned_owner_match.group(1))
                        
              
                cap_number_match = re.search(r'\bD\d+\s+', line)
                if cap_number_match:
                    cap_number = cap_number_match.group().strip()
                    columns = line.split()
                    if len(columns) >= 4:  # Check if line contains enough columns
                        amount_requested = columns[1]
                        received_date = columns[3]
                        last_active_date = columns[2]
                        data_tuples.append((cap_number, assigned_owner, received_date, last_active_date, report_date))
        
        return data_tuples

def tuples_to_json(data_tuples):
    json_data = []
    for data_tuple in data_tuples:
        json_entry = {
            "D#": data_tuple[0],
            "Status": data_tuple[1],
            "Received Date": data_tuple[2],
            "Last Active Date": data_tuple[3],
            "Report Date": data_tuple[4]
        }
        json_data.append(json_entry)
        print(json_entry)

    return json_data


pdf_file = 'pdfReports/12042023.pdf'
data_tuples = extract_data_from_pdf(pdf_file)
json_data = tuples_to_json(data_tuples)


with open('./Json Data/12042023.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)


print('Data transferred to data.json as tuples')
