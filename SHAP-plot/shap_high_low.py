import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
file_path = '/home/stefan/Documents/zjzpa-analiza-main/main/high_low.csv'
data = pd.read_csv(file_path)

# Filter out the 'Lowest' values
highest_data = data[data['Substance'].str.contains('Highest')]

# Simplify the substance names by removing the 'Highest ' prefix
highest_data['Substance'] = highest_data['Substance'].str.replace('Highest ', '', regex=False)

# Process the data
# Pivot the data to get it into a format suitable for a heatmap
pivot_table = highest_data.pivot_table(index='Substance', columns='Date', values='Value')

# Sort the substances by their maximum values to display highest values at the top
sorted_index = pivot_table.max(axis=1).sort_values(ascending=False).index
sorted_pivot_table = pivot_table.loc[sorted_index]

# Generate the heatmap
plt.figure(figsize=(12, 8))
heatmap = sns.heatmap(sorted_pivot_table, annot=True, cmap='coolwarm', fmt='.1f', linewidths=0.5, cbar_kws={'label': 'Value'})

# Customize the plot
plt.title(
    'Najvisa zabelezena vrednost suspendovanih cestica u naselju Streliste 2017-2024 god\n'
    '2524 pdfa, 40747 vrednosti analizirano',
    fontsize=12,  # Adjusted font size
    pad=20        # Adjust padding to position title
)
plt.xlabel('Datum zabelezene najvece vrednosti')
plt.ylabel('Suspendovane cestice PM2.5µg/m3')

# Save the plot as PNG
output_path = '/home/stefan/Documents/zjzpa-analiza-main/main/SHAP-plot/heatmap_highest.png'
plt.savefig(output_path)

# Show the plot (optional)
plt.show()

