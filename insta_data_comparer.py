#%%
import pandas as pd

# Load the two CSV files into separate DataFrames
df_x = pd.read_csv('followers_data_03_04_2024.csv')
df_y = pd.read_csv('followers_data.csv')

# Use merge with indicator to find rows not in both
merged_df = pd.merge(df_x, df_y, how='outer', indicator=True)

# Filter the merged DataFrame to keep rows that are not in both
unique_df = merged_df[merged_df['_merge'] != 'both']

# Drop the '_merge' column used for filtering
unique_df = unique_df.drop(columns=['_merge'])

print(unique_df)

# %%
unique_df.to_csv("compare.csv")
# %%
