import pandas as pd

# Load the CSV files
topic_slugs = pd.read_csv('topic_slugs.csv')
topic_page_traffic = pd.read_csv('topic_page_traffic.csv')

# Merge the files
# 1. Keep traffic data from topic_page_traffic.csv as is.
# 2. Add unique slugs from topic_slugs.csv with traffic set to 0.
# Combine both datasets
merged = pd.concat([
    topic_page_traffic,
    topic_slugs[~topic_slugs['slug'].isin(topic_page_traffic['slug'])]
])

# Assign 0 traffic for slugs unique to topic_slugs.csv
merged['traffic'] = merged['traffic'].fillna(0).astype(int)

# Save the merged file
merged.to_csv('merged_topic_data.csv', index=False)

print("Merged file saved as 'merged_topic_data.csv'")
