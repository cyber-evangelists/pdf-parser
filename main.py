import re
from pypdf import PdfReader
import json

def extract_data_from_pdf(pdf_file):
    """
    Extract data from a PDF file containing an invoice report.

    Args:
        pdf_file (str): Path to the PDF file.

    Returns:
        list: A list of tuples containing extracted data.
            Each tuple contains information about a single entry in the report.
            Tuple format: (D#, Assigned Owner, Received Date, Last Active Date, Report Date).
    """
    with open(pdf_file, 'rb') as file:
        reader = PdfReader(file)
        report_date = None
        data_tuples = []

        for page in reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                # Check if the line contains the report date
                if "Invoice Report by Contractor" in line:
                    report_date_match = re.search(r'(\d{2}/\d{2}/\d{4})$', line)
                    if report_date_match:
                        report_date = report_date_match.group(1)
                
                # Check if the line contains the Assigned Owner
                if "Assigned Owner" in line:
                    # assigned_owner_match = re.search(r'Assigned Owner (A\d{5})', line)
                    assigned_owner_match = re.search(r'Assigned Owner A\d{5}\s+(.+)$', line)
                    if assigned_owner_match:
                        assigned_owner = "Assigned Owner " + assigned_owner_match.group(1)
                        
                # Check if the line contains the CAP number
                cap_number_match = re.search(r'\bD\d+\s+', line)
                if cap_number_match:
                    cap_number = cap_number_match.group().strip()
                    columns = line.split()
                    if len(columns) >= 4:  # Check if line contains enough columns
                        amount_requested = columns[1]
                        received_date = columns[3]
                        last_active_date = columns[2]
                        # Append extracted data to data_tuples
                        data_tuples.append((cap_number, assigned_owner, received_date, last_active_date, report_date))
        
        return data_tuples

def tuples_to_json(data_tuples):
    """
    Convert extracted data tuples to JSON format.

    Args:
        data_tuples (list): List of tuples containing extracted data.

    Returns:
        list: A list of dictionaries, each representing an entry in JSON format.
    """
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


# Example usage
pdf_file = 'your_pdf.pdf'
data_tuples = extract_data_from_pdf(pdf_file)
json_data = tuples_to_json(data_tuples)

# Write JSON data to a file
with open('./Json Data/01032024 DOE Report.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print('Data transferred to JSON file.')
