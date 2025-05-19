import pandas as pd

# Load the CSV file
file_path = "topic_slugs.csv"  # Replace with your file path
df = pd.read_csv(file_path)

# Specify the column to modify
column_to_modify = "slug"  # Replace with the column name

# Concatenate '/t/' in front of each line in the specified column
df[column_to_modify] = "/t/" + df[column_to_modify].astype(str)

# Save the updated DataFrame back to a CSV file
output_path = "updated_file.csv"
df.to_csv(output_path, index=False)

print(f"Updated CSV file saved to {output_path}")
