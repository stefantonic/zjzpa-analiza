import pandas as pd
import numpy as np

# Load the data from the CSV file
input_file = 'output.csv'
data = pd.read_csv(input_file)

# Map incorrect substance names to correct ones
name_corrections = {
    'NO': 'NO2',
    # Add other name corrections here if needed
}

# Apply the corrections to the 'Substance' column
data['Substance'] = data['Substance'].replace(name_corrections)

# Define which column index to use for each substance
substance_column_mapping = {
    'SO2': 3,
    'ČAĐ': 3,
    'NO2': 3,
    'NH3': 2,
    'TSP': 2,
    'PM10': 2,
    'BC': 1,
    'UV': 1,
    'Benzen': 1
}

# Function to calculate the median value for each substance
def calculate_median_per_substance(df):
    result = []
    
    # Create a DataFrame to maintain the order of substances
    order_df = df[['Substance']].drop_duplicates().reset_index(drop=True)
    order_df['Order'] = order_df.index
    
    # Filter out 'Benzen' entries with '1god'
    df_filtered = df[~((df['Substance'] == 'Benzen') & (df['Period'] == '1god'))]
    
    # Track max and min values for each relevant substance
    max_values = {}
    min_values = {}
    
    # Process each substance
    for substance, group in df_filtered.groupby('Substance'):
        if substance in substance_column_mapping:
            column_index = substance_column_mapping[substance]
            column_name = f'Value{column_index}'
            values = group[column_name].dropna()
            
            # Track max and min values
            if not values.empty:
                max_value = values.max()
                min_value = values.min()
                
                if substance not in max_values:
                    max_values[substance] = max_value
                else:
                    max_values[substance] = max(max_values[substance], max_value)
                
                if substance not in min_values:
                    min_values[substance] = min_value
                else:
                    min_values[substance] = min(min_values[substance], min_value)

                median_value = np.median(values)
            else:
                median_value = 0.0
            
            result.append({
                'Substance': substance,
                'Median Value': median_value
            })
        else:
            # Handle any substances not in the mapping if needed
            values = pd.concat([group['Value1'], group['Value2'], group['Value3'], group['Value4']])
            values = values.dropna()
            if not values.empty:
                median_value = np.median(values)
            else:
                median_value = 0.0
            result.append({
                'Substance': substance,
                'Median Value': median_value
            })
    
    # Convert result to DataFrame
    result_df = pd.DataFrame(result)
    
    # Add rows for highest and lowest values (if needed, otherwise comment out this section)
    high_low_rows = []
    for substance in ['SO2', 'ČAĐ', 'NO2', 'NH3', 'TSP', 'PM10', 'BC', 'UV', 'Benzen']:
        if substance in max_values:
            high_low_rows.append({'Substance': f'Highest {substance}', 'Median Value': max_values[substance]})
            high_low_rows.append({'Substance': f'Lowest {substance}', 'Median Value': min_values[substance]})
    
    high_low_df = pd.DataFrame(high_low_rows)
    result_df = pd.concat([result_df, high_low_df], ignore_index=True)
    
    # Merge with the order DataFrame to maintain original order
    result_df = result_df.merge(order_df, on='Substance', how='left').sort_values(by='Order').drop(columns='Order')
    
    return result_df

# Calculate the median value for each substance
median_per_substance = calculate_median_per_substance(data)

# Add additional columns for the output CSV
median_per_substance['Date Calculated'] = pd.Timestamp.now().strftime('%d.%m.%Y')
median_per_substance['Period'] = 'N/A'

# Filter out rows with 'Highest' and 'Lowest'
median_per_substance = median_per_substance[~median_per_substance['Substance'].str.contains('Highest|Lowest')]

# Save the results to a new CSV file
output_file = 'median.csv'
median_per_substance.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")

