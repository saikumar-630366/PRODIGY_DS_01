import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for better visualization
plt.style.use('seaborn-v0_8')

# Load the population data
population_data = pd.read_csv('data/PRODIGY_DS_01-main/API_SP.POP.TOTL_DS2_en_csv_v2_26346.csv', skiprows=3)
metadata = pd.read_csv('data/PRODIGY_DS_01-main/Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_26346.csv')

# Process the data
# Get the latest year's population data (2023)
latest_population = population_data[['Country Name', '2023']].copy()
latest_population.columns = ['Country', 'Population']

# Merge with metadata to get region information
merged_data = latest_population.merge(metadata[['TableName', 'Region']], 
                                    left_on='Country', 
                                    right_on='TableName', 
                                    how='inner')

# Remove rows where Region is empty and drop duplicates
merged_data = merged_data.dropna(subset=['Region']).drop_duplicates(subset=['Country'])

# Create a figure with two subplots side by side
plt.figure(figsize=(15, 6))

# Plot 1: Distribution of Population by Country
plt.subplot(1, 2, 1)
plt.hist(np.log10(merged_data['Population']), bins=30, edgecolor='black')
plt.title('Distribution of Country Populations (Log Scale)')
plt.xlabel('Log10(Population)')
plt.ylabel('Number of Countries')

# Plot 2: Population by Region
plt.subplot(1, 2, 2)
region_population = merged_data.groupby('Region')['Population'].sum().sort_values(ascending=True)
plt.barh(region_population.index, np.log10(region_population.values))
plt.title('Total Population by Region (Log Scale)')
plt.xlabel('Log10(Population)')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()