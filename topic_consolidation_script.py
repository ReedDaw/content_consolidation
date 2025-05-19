import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
from tqdm import tqdm

# Function to preprocess and combine relevant fields
def preprocess_data(df):
    # Combine title tag and topic summary for similarity analysis
    df['combined_text'] = (
        df['title_tag'].fillna('') + ' ' +
        df['topic_summary'].fillna('')
    )
    return df

# Function to compute text similarity and cluster
def cluster_topic_pages(df):
    # Vectorize combined text using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(df['combined_text'])
    
    # Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    # Ensure values are in range [0, 1]
    similarity_matrix = similarity_matrix.clip(0, 1)
    
    # Convert similarity to dissimilarity (1 - similarity)
    dissimilarity_matrix = 1 - similarity_matrix
    
    # Apply DBSCAN clustering
    clustering_model = DBSCAN(eps=0.5, min_samples=2, metric='precomputed')
    clusters = clustering_model.fit_predict(dissimilarity_matrix)
    
    df['cluster'] = clusters
    return df

# Function to create canonical mapping
def create_canonical_mapping(df):
    canonical_mapping = []
    
    for cluster_id, group in tqdm(df.groupby('cluster')):
        if cluster_id == -1:  # Skip noise points
            continue
        
        # Identify the canonical page (highest traffic)
        canonical_page = group.loc[group['traffic'].idxmax()]['url']
        
        # List all duplicate pages (including the canonical page itself)
        duplicate_pages = group['url'].tolist()
        
        # Remove the canonical page from the duplicate list for clarity
        duplicate_pages.remove(canonical_page)
        
        # Append canonical mapping
        canonical_mapping.append({
            'canonical_page': canonical_page,
            'duplicate_pages': ', '.join(duplicate_pages)
        })
    
    return pd.DataFrame(canonical_mapping)

# Main function
def process_topic_pages(file_path, output_path):
    # Load data
    print("Loading data...")
    df = pd.read_csv(file_path)
    
    # Preprocess data
    print("Preprocessing data...")
    df = preprocess_data(df)
    
    # Cluster topic pages
    print("Clustering topic pages...")
    df = cluster_topic_pages(df)
    
    # Create canonical mapping
    print("Creating canonical mapping...")
    canonical_mapping = create_canonical_mapping(df)
    
    # Save results
    print("Saving results...")
    canonical_mapping.to_csv(output_path, index=False)
    print(f"Canonical mapping saved to {output_path}")

# Example usage
if __name__ == "__main__":
    input_file = "topic_pages.csv"  # Replace with your input file
    output_file = "canonical_topic_pages.csv"  # Output file for canonical pages
    process_topic_pages(input_file, output_file)
