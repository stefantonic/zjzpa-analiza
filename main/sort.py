import csv
import re

def parse_line(line):
    # Updated regular expression to better capture substances with spaces
    pattern = r'^(.+?)\s+(\d+ ?\w+)\s+mg/m3(?:\s*(\d{2}\.\d{2}\.\d{4}))?\s*(\d+)?\s*(\d+)?\s*(\d+)?\s*(\d+)?'
    
    match = re.match(pattern, line)
    if match:
        substance = match.group(1).strip()
        period = match.group(2).strip()
        date = match.group(3).strip() if match.group(3) else ''
        values = [match.group(i) or '' for i in range(4, 8)]
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
            if re.match(r'^(.+?)\s+(\d+ ?\w+)\s+mg/m3', line):
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

