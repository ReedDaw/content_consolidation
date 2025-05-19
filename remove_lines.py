import pandas as pd

# Load the CSV file
file_path = "topic_page_slugs.csv"  # Replace with your file path
df = pd.read_csv(file_path)

# Specify the column to check
column_to_filter = "slug"  # Replace with the column name

# Filter rows that end with "-en-us"
df_filtered = df[df[column_to_filter].str.endswith("-en-us", na=False)]

# Save the filtered DataFrame back to a CSV file
output_path = "filtered_file.csv"
df_filtered.to_csv(output_path, index=False)

print(f"Filtered CSV file saved to {output_path}")
