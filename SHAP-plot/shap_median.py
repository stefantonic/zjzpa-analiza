import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Read the CSV file
file_path = '/home/stefan/Documents/zjzpa-analiza-main/main/median.csv'
data = pd.read_csv(file_path)

# Display the data to understand its structure
print(data)

# Define the exact order of substances, including only 'Benzene' and removing 'Benzen'
substances_of_interest = ['SO 2', 'ČAĐ', 'NO2', 'NH3', 'BC', 'UV', 'Benzene']
filtered_data = data[data['Substance'].isin(substances_of_interest)]

# Map 'Median Value' to categories
def categorize_value(value):
    if value == 0:
        return 'Good'
    elif value <= 35.5:
        return 'Moderate'
    elif value <= 55.5:
        return 'Unhealthy'
    else:
        return 'Very Unhealthy'  # Extend this if needed

# Apply the categorization
filtered_data['Category'] = filtered_data['Median Value'].apply(categorize_value)

# Pivot the data for the heatmap
heatmap_data = filtered_data.pivot(index='Substance', columns='Category', values='Median Value')

# Ensure all values are numeric
heatmap_data = heatmap_data.apply(pd.to_numeric, errors='coerce')

# Calculate the median value for each substance
median_values = filtered_data.groupby('Substance')['Median Value'].max()

# Sort substances based on median values from highest to lowest
sorted_substances = median_values.sort_values(ascending=False).index

# Reorder the DataFrame to match the sorted substances
heatmap_data = heatmap_data.reindex(sorted_substances)

# Display the pivot table to verify
print(heatmap_data)

# Define custom colormap
cmap = plt.get_cmap("coolwarm")
colors = cmap(np.linspace(0, 1, cmap.N))

# Plot the heatmap
plt.figure(figsize=(12, 8))
ax = sns.heatmap(heatmap_data, annot=True, cmap=cmap, fmt='.1f', cbar=True, 
                 yticklabels=sorted_substances)

# Set labels and title
plt.xlabel('Kategorija')
plt.ylabel('Suspendovane cestice PM2.5µg/m3')
plt.title(
    'Srednja vrednost suspendovanih cestica u naselju Streliste 2017-2024 god;\n'
    '2524 pdfa; 40747 vrednosti analizirano',
    pad=20  # Adjust the padding to move the title away from the plot
)

# Save the plot if needed
plt.savefig('/home/stefan/Documents/zjzpa-analiza-main/main/SHAP-plot/heatmap_median_values.png')

# Show the plot
plt.show()

