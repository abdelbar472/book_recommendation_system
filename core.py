# core.py
import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from tqdm import tqdm

# ========================
# Configuration
# ========================
CSV_FILE = "books.csv"
EMBEDDINGS_FILE = "embeddings.npy"
COLLECTION_NAME = "books"
QDRANT_HOST = "localhost"   # Use "qdrant" if running inside Docker network
QDRANT_PORT = 6333
QDRANT_API_KEY = "diaphragms2025"  # Remove or set to None if no API key

# ========================
# Load and Clean Data
# ========================
print("Loading and cleaning books data...")
df = pd.read_csv(CSV_FILE, low_memory=False)

df = df.rename(columns={
    'Book-Title': 'title',
    'Book-Author': 'authors',
    'Year-Of-Publication': 'year',
    'Publisher': 'publisher',
    'Image-URL-M': 'image_url',
})

df['year'] = pd.to_numeric(df['year'], errors='coerce')
df = df.dropna(subset=['title', 'authors', 'year'])
df = df[(df['year'] > 1800) & (df['year'] <= 2025)]
df = df.drop_duplicates(subset=['title', 'authors', 'year'])
df = df.reset_index(drop=True)

df['text'] = df.apply(
    lambda row: f"Title: {row['title']}. "
                f"Author: {row['authors']}. "
                f"Published: {int(row['year'])}. "
                f"Publisher: {row.get('publisher', 'Unknown')}.",
    axis=1
)

books = df.to_dict('records')
print(f"Prepared {len(books):,} books.\n")

# ========================
# Embedding Model & Cache
# ========================
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

if os.path.exists(EMBEDDINGS_FILE):
    print("Loading cached embeddings...")
    embeddings = np.load(EMBEDDINGS_FILE)
else:
    print("Generating embeddings (first time only)...")
    embeddings = model.encode(df['text'].tolist(), batch_size=32, show_progress_bar=True)
    np.save(EMBEDDINGS_FILE, embeddings)
    print("Embeddings saved for future runs.\n")

# ========================
# Qdrant Connection & Indexing
# ========================
print("Connecting to Qdrant...")
client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
    api_key=QDRANT_API_KEY if QDRANT_API_KEY else None,
    https=False,
    timeout=60,
)

if not client.collection_exists(COLLECTION_NAME):
    print("Creating collection and uploading...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    points = [
        PointStruct(
            id=i,
            vector=vector.tolist(),
            payload={
                "title": book['title'],
                "authors": book['authors'],
                "year": int(book['year']),
                "publisher": book.get('publisher', 'Unknown'),
                "image_url": book.get('image_url', ''),
            }
        )
        for i, (book, vector) in enumerate(zip(books, embeddings))
    ]

    batch_size = 100
    for i in tqdm(range(0, len(points), batch_size), desc="Uploading"):
        client.upsert(collection_name=COLLECTION_NAME, points=points[i:i + batch_size])

    print("Upload complete!\n")
else:
    print("Collection exists — ready to serve!\n")

# Export for API
__all__ = ['client', 'collection_name', 'model', 'books']