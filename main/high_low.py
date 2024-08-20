import pandas as pd

# Load the data from the output.csv file
input_file = 'output.csv'
data = pd.read_csv(input_file, header=None, names=['Substance', 'Period', 'Date', 'Value1', 'Value2', 'Value3', 'Value4'])

# Define the order for substances, including both 'Benzen' and 'Benzene'
substance_order = ['SO 2', 'ČAĐ', 'NO2', 'NH3', 'TSP', 'PM10', 'BC', 'UV', 'Benzen', 'Benzene']

# Initialize dictionaries to store highest and lowest values with corresponding dates
highest_values = {}
lowest_values = {}

# Process each substance to find the highest and lowest values
for substance in substance_order:
    substance_data = data[data['Substance'].str.strip() == substance]

    if not substance_data.empty:
        all_values = []
        all_dates = []

        for column in ['Value1', 'Value2', 'Value3', 'Value4']:
            if column in substance_data.columns:
                for idx, row in substance_data.iterrows():
                    value = row[column]
                    if pd.notna(value):
                        all_values.append(float(value))
                        all_dates.append(row['Date'])

        if all_values:
            values_df = pd.DataFrame({'Value': all_values, 'Date': all_dates})
            highest_row = values_df.loc[values_df['Value'].idxmax()]
            lowest_row = values_df.loc[values_df['Value'].idxmin()]

            highest_values[substance] = (highest_row['Value'], highest_row['Date'])
            lowest_values[substance] = (lowest_row['Value'], lowest_row['Date'])

# Process Benzen separately (second value after ,,)
benzen_data = data[data['Substance'].str.strip() == 'Benzen']

if not benzen_data.empty:
    benzen_values = []

    for idx, row in benzen_data.iterrows():
        value = row['Value2']  # Use second value after the first ,,,
        if pd.notna(value):
            benzen_values.append(float(value))

    if benzen_values:
        highest_benzen = max(benzen_values)
        lowest_benzen = min(benzen_values)
        
        # Example dates for Benzen
        highest_date_benzen = benzen_data[benzen_data['Value2'] == highest_benzen]['Date'].values[0]
        lowest_date_benzen = benzen_data[benzen_data['Value2'] == lowest_benzen]['Date'].values[0]

        highest_values['Benzen'] = (highest_benzen, highest_date_benzen)
        lowest_values['Benzen'] = (lowest_benzen, lowest_date_benzen)

# Process Benzene separately (third value after ,,,)
benzene_data = data[data['Substance'].str.strip() == 'Benzene']

if not benzene_data.empty:
    benzene_values = []

    for idx, row in benzene_data.iterrows():
        value = row['Value3']  # Use third value after the first ,,,
        if pd.notna(value):
            benzene_values.append(float(value))

    if benzene_values:
        highest_benzene = max(benzene_values)
        lowest_benzene = min(benzene_values)
        
        # Example dates for Benzene
        highest_date_benzene = benzene_data[benzene_data['Value3'] == highest_benzene]['Date'].values[0]
        lowest_date_benzene = benzene_data[benzene_data['Value3'] == lowest_benzene]['Date'].values[0]

        highest_values['Benzene'] = (highest_benzene, highest_date_benzene)
        lowest_values['Benzene'] = (lowest_benzene, lowest_date_benzene)

# Prepare the result DataFrame
result = []

# Add highest values for each substance in the specified order
for substance in substance_order:
    if substance in highest_values:
        highest_value, highest_date = highest_values[substance]
        result.append({
            'Substance': f'Highest {substance}',
            'Period': '24h',
            'Date': highest_date,
            'Value': highest_value
        })

# Add lowest values for each substance in the specified order
for substance in substance_order:
    if substance in lowest_values:
        lowest_value, lowest_date = lowest_values[substance]
        result.append({
            'Substance': f'Lowest {substance}',
            'Period': '24h',
            'Date': lowest_date,
            'Value': lowest_value
        })

# Convert result to DataFrame
result_df = pd.DataFrame(result, columns=['Substance', 'Period', 'Date', 'Value'])

# Define a custom sorting function
def sort_key(value):
    parts = value.split()
    if len(parts) < 2:
        return (1, float('inf'))
    rank = 0 if parts[0] == 'Highest' else 1
    substance = ' '.join(parts[1:])
    if substance in substance_order:
        return (rank, substance_order.index(substance))
    return (rank, len(substance_order) + 1)

# Apply custom sorting
result_df = result_df.sort_values(by=['Substance'], key=lambda x: x.map(lambda val: sort_key(val)))

# Save the results to a new CSV file
output_file = 'high_low.csv'
result_df.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")

