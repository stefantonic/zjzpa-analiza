import pandas as pd

# Load the data from the output.csv file
input_file = 'output.csv'
data = pd.read_csv(input_file, header=None, names=['Substance', 'Period', 'Date', 'Value1', 'Value2', 'Value3', 'Value4'])

# Define the order for substances
substance_order = ['SO 2', 'ČAĐ', 'NO2', 'NH3', 'TSP', 'PM10', 'BC', 'UV', 'Benzen']

# Initialize dictionaries to store highest and lowest values with corresponding dates
highest_values = {}
lowest_values = {}

# Process each substance to find the highest and lowest values
for substance in substance_order:
    # Ensure we handle 'SO2' and other substances correctly
    substance_data = data[data['Substance'].str.strip() == substance]

    if not substance_data.empty:
        # Initialize lists to gather values and dates
        all_values = []
        all_dates = []

        # Gather all non-null values and dates for this substance
        for column in ['Value1', 'Value2', 'Value3', 'Value4']:
            if column in substance_data.columns:
                for idx, row in substance_data.iterrows():
                    # Process the value only if it's not null
                    value = row[column]
                    if pd.notna(value):
                        all_values.append(float(value))  # Convert to float for comparison
                        all_dates.append(row['Date'])

        if all_values:
            # Convert lists to DataFrame for processing
            values_df = pd.DataFrame({
                'Value': all_values,
                'Date': all_dates
            })
            
            # Find the highest and lowest values and their dates
            if not values_df.empty:
                highest_row = values_df.loc[values_df['Value'].idxmax()]
                lowest_row = values_df.loc[values_df['Value'].idxmin()]

                # Store the results
                highest_values[substance] = (highest_row['Value'], highest_row['Date'])
                lowest_values[substance] = (lowest_row['Value'], lowest_row['Date'])

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
    # Split the string to separate "Highest" and "Lowest" from the substance
    parts = value.split()
    if len(parts) < 2:
        return (1, float('inf'))  # Handle unexpected values safely
    rank = 0 if parts[0] == 'Highest' else 1
    substance = ' '.join(parts[1:])
    # Ensure the substance is in the substance_order list
    if substance in substance_order:
        return (rank, substance_order.index(substance))
    return (rank, len(substance_order))  # Default rank for unknown substances

# Apply custom sorting
result_df = result_df.sort_values(by=['Substance'], key=lambda x: x.map(lambda val: sort_key(val)))

# Save the results to a new CSV file
output_file = 'sorted_median.csv'
result_df.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")

