import pandas as pd
import re
from collections import defaultdict

# Load the CSV file
def load_data(file_path):
    """Load slug and traffic data from a CSV file."""
    data = pd.read_csv(file_path, usecols=["slug", "traffic"])
    return data

def clean_slug(slug):
    """Clean the slug to remove numbers or country codes."""
    # Remove numbers at the end
    slug = re.sub(r"-\d+$", "", slug)
    # Remove country codes
    slug = re.sub(r"-en-[a-z]{2}$", "", slug)
    return slug

def cluster_slugs(data):
    """Group similar slugs and select the canonical slug with the highest traffic."""
    grouped = defaultdict(list)
    for _, row in data.iterrows():
        base_slug = clean_slug(row["slug"])
        grouped[base_slug].append((row["slug"], row["traffic"]))

    # Select the canonical slug with the highest traffic for each cluster
    canonical_clusters = []
    for cluster, items in grouped.items():
        canonical_slug = max(items, key=lambda x: x[1])[0]  # Select slug with max traffic
        for slug, traffic in items:
            canonical_clusters.append([cluster, canonical_slug, slug, traffic])

    return canonical_clusters

def save_clusters_to_csv(clusters, output_file):
    """Save clustered slugs to a CSV file."""
    df = pd.DataFrame(clusters, columns=["Cluster", "Canonical_Slug", "Slug", "Traffic"])
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # File paths
    input_file = "merged_topic_data.csv"
    output_file = "slug_clusters_with_canonical.csv"

    print("Loading data...")
    data = load_data(input_file)

    print("Clustering slugs...")
    clusters = cluster_slugs(data)

    print("Saving clusters to CSV...")
    save_clusters_to_csv(clusters, output_file)

    print(f"Processing complete. Clusters saved to {output_file}.")
