import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define file paths
input_file_path = '/home/stefan/Desktop/zjzpa-analiza-main/main/output.csv'
output_dir = '/home/stefan/Desktop/zjzpa-analiza-main/main/PM2.5/'

# Load the data from the CSV file
data = pd.read_csv(input_file_path)

# Ensure the necessary columns exist
required_columns = ['Substance', 'Value1', 'Value2', 'Value3', 'Value4']
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"The input CSV must contain the columns: {', '.join(required_columns)}")

# Define a function to determine the value based on the substance
def get_value(row):
    if row['Substance'] == 'BC' or row['Substance'] == 'UV':
        return row['Value1']
    elif row['Substance'] == 'Benzene':
        return row['Value2']
    else:
        if not pd.isna(row['Value4']):
            return row['Value4']
        elif not pd.isna(row['Value3']):
            return row['Value3']
        else:
            return np.nan

# Apply the function to create the 'Value' column
data['Value'] = data.apply(get_value, axis=1)

# Remove rows where 'Substance' is 'TSP' but keep 'Benzene'
data = data[(data['Substance'] != 'TSP') | (data['Substance'] == 'Benzene')]

# Generate a pcolormesh plot for each substance and save as PNG
for i, substance in enumerate(data['Substance'].unique(), start=1):
    subset = data[data['Substance'] == substance]
    
    # Remove rows where 'Value' is NaN
    subset = subset.dropna(subset=['Value'])
    
    # Ensure the subset is not empty
    if subset.empty:
        print(f"No data available for {substance}. Skipping...")
        continue
    
    # Ensure index is numeric (reset if necessary)
    if subset.index.dtype != np.int64:
        subset = subset.reset_index(drop=True)
    
    # Prepare data for pcolormesh
    x = subset.index
    y = subset['Value']
    
    # Ensure x and y do not contain NaN or infinite values
    if len(x) == 0 or len(y) == 0 or np.any(np.isnan(x)) or np.any(np.isnan(y)) or np.any(np.isinf(x)) or np.any(np.isinf(y)):
        print(f"Data for {substance} contains non-finite values. Skipping...")
        continue
    
    # Create 2D histogram
    # Define bins
    x_bins = np.linspace(min(x), max(x), 100)
    y_bins = np.linspace(min(y), max(y), 100)
    
    # Compute 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[x_bins, y_bins])
    
    plt.figure(figsize=(10, 8))
    
    # Plot pcolormesh
    plt.pcolormesh(x_edges, y_edges, hist.T, shading='auto', cmap='coolwarm')
    
    # Add color bar
    plt.colorbar(label='Gustina')
    
    # Title with bold substance
    plt.title(
        f'Individualna reprezentacija progresije i koncentracije suspendovane cestice {substance};    \n'
        f'period analize 2017-2024 god; indeks 0 do 101866(velicina dataseta)', 
        fontsize=12, 
        loc='center'
    )
    plt.xlabel('Indeks')
    plt.ylabel('Vrednost')
    
    # Save the plot to a PNG file with a unique name
    output_file_path = f'{output_dir}pcolormesh_{i}.png'
    plt.savefig(output_file_path)
    
    # Optionally show the plot (comment out if not needed)
    # plt.show()
    
    # Close the plot to free up memory
    plt.close()

