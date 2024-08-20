import csv
import re

def parse_line(line):
    # Updated regular expression to handle substances and values after # #
    pattern_general = r'^(.+?)\s+(\d+ ?\w+)\s+mg/m3(?:\s*(\d{2}\.\d{2}\.\d{4}))?\s*(\d+)?\s*(\d+)?\s*(\d+)?\s*(\d+)?'
    pattern_benzene = r'^Benzen\s+(\d+ ?\w+)\s+mg/m3# #\s*(\d+)\s+(\d+)'
    
    # Check for Benzene first
    match_benzene = re.match(pattern_benzene, line)
    if match_benzene:
        substance = "Benzene"
        period = match_benzene.group(1).strip()
        date = ''  # Benzene pattern does not include a date
        value2 = match_benzene.group(3).strip()  # Always take the second value after #
        return [substance, period, date, '', value2, '', '']

    # General case
    match_general = re.match(pattern_general, line)
    if match_general:
        substance = match_general.group(1).strip()
        period = match_general.group(2).strip()
        date = match_general.group(3).strip() if match_general.group(3) else ''
        values = [match_general.group(i) or '' for i in range(4, 8)]
        return [substance, period, date] + values
    
    return None

def extract_data_from_file(filename):
    extracted_data = []
    with open(filename, 'r') as file:
        temp_data = []
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            # Check if line matches expected pattern for new entry
            if re.match(r'^(.+?)\s+(\d+ ?\w+)\s+mg/m3', line) or re.match(r'^Benzen\s+', line):
                # Process previous multi-line entry if it exists
                if temp_data:
                    combined = ' '.join(temp_data)
                    parsed_data = parse_line(combined)
                    if parsed_data:
                        extracted_data.append(parsed_data)
                    temp_data = []

                # Start a new entry
                temp_data.append(line)
            else:
                # Continuation of a multi-line entry
                temp_data.append(line)

        # Process last entry if any
        if temp_data:
            combined = ' '.join(temp_data)
            parsed_data = parse_line(combined)
            if parsed_data:
                extracted_data.append(parsed_data)
    
    return extracted_data

def filter_data(data):
    filtered_data = [entry for entry in data if entry[1] != '1god']
    return filtered_data

def write_to_csv(data, output_filename):
    header = ['Substance', 'Period', 'Date', 'Value1', 'Value2', 'Value3', 'Value4']
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

def main(input_filename, output_filename):
    data = extract_data_from_file(input_filename)
    filtered_data = filter_data(data)
    write_to_csv(filtered_data, output_filename)

# Replace 'input.txt' and 'output.csv' with your file names
if __name__ == "__main__":
    main('/home/stefan/Desktop/main/output.txt', 'output.csv')

