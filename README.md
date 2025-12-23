# Book Recommendation System 📚

A content-based book recommendation system using vector embeddings and semantic search with Qdrant vector database.

## 🎯 Overview

This system recommends books based on semantic similarity using machine learning embeddings. When you provide a book title, the system finds similar books by comparing their vector representations in high-dimensional space.

## ✨ Features

- **Semantic Search**: Find books by meaning, not just keywords
- **Fast API**: RESTful API built with FastAPI
- **Vector Database**: Powered by Qdrant for efficient similarity search
- **Rich Metadata**: Includes title, author, year, publisher, and cover images
- **Smart Caching**: Embeddings are generated once and cached for fast startup
- **Duplicate Filtering**: Removes duplicate recommendations intelligently
- **Author Filtering**: Option to exclude books by the same author

## 🏗️ Architecture

```
┌─────────────┐
│   FastAPI   │  ← REST API Layer
└──────┬──────┘
       │
┌──────▼──────┐
│  Core Logic │  ← Embedding & Search
└──────┬──────┘
       │
┌──────▼──────┐
│   Qdrant    │  ← Vector Database
└─────────────┘
```

## 📊 Dataset

- **Source**: Book-Crossing dataset
- **Size**: ~266,000+ books
- **Columns**: ISBN, Title, Author, Year, Publisher, Image URLs
- **Preprocessing**: Cleaned invalid years, removed duplicates

## 🛠️ Technology Stack

- **Python 3.12**
- **FastAPI**: Modern web framework for APIs
- **Sentence Transformers**: `all-MiniLM-L6-v2` for embeddings (384 dimensions)
- **Qdrant**: Vector database for similarity search
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations
- **Uvicorn**: ASGI server

## 📦 Installation

### Prerequisites

- Python 3.8+
- Docker (for Qdrant)

### 1. Clone Repository

```bash
git clone https://github.com/abdelbar472/book_recommendation_system.git
cd book_recommendation_system
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn sentence-transformers qdrant-client pandas numpy tqdm
```

### 4. Start Qdrant (Docker)

```bash
docker run -d -p 6333:6334 \
  -e QDRANT__SERVICE__API_KEY=diaphragms2025 \
  -v qdrant_storage:/qdrant/storage \
  --name qdrant \
  qdrant/qdrant:latest
```

### 5. Prepare Data

Place `books.csv` in the project root directory.

## 🚀 Usage

### Start the API Server

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Access the API

- **Interactive Docs**: http://localhost:8000/docs
- **API Base**: http://localhost:8000

### API Endpoints

#### 1. Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "books_loaded": 266723,
  "qdrant_collection": true
}
```

#### 2. Get Recommendations

```bash
POST /recommend
```

**Request Body:**
```json
{
  "title_substring": "Harry Potter",
  "top_k": 8,
  "skip_same_author": false
}
```

**Response:**
```json
{
  "seed_book": "Harry Potter and the Sorcerer's Stone by J.K. Rowling (1998)",
  "recommendations": [
    {
      "title": "Harry Potter and the Chamber of Secrets",
      "authors": "J.K. Rowling",
      "year": 1999,
      "publisher": "Scholastic",
      "similarity": 0.9234
    }
  ]
}
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "title_substring": "1984",
    "top_k": 5,
    "skip_same_author": false
  }'
```

### Python Example

```python
import requests

response = requests.post(
    "http://localhost:8000/recommend",
    json={
        "title_substring": "The Great Gatsby",
        "top_k": 10,
        "skip_same_author": True
    }
)

data = response.json()
print(f"Based on: {data['seed_book']}\n")
for rec in data['recommendations']:
    print(f"• {rec['title']} by {rec['authors']} ({rec['year']})")
    print(f"  Similarity: {rec['similarity']}\n")
```

## 🔍 How It Works

### 1. Data Preparation
- Load books from CSV
- Clean and normalize data (years, duplicates)
- Create rich text descriptions for each book

### 2. Embedding Generation
- Use `all-MiniLM-L6-v2` model to convert book descriptions into 384-dimensional vectors
- Cache embeddings to disk (`embeddings.npy`) for fast reloads

### 3. Vector Indexing
- Store vectors in Qdrant with metadata (title, author, year, etc.)
- Use cosine similarity for distance metric

### 4. Recommendation Process
- User provides a book title
- System finds matching book in database
- Converts book to embedding vector
- Searches Qdrant for nearest neighbors
- Returns top-k most similar books with scores

## 📁 Project Structure

```
simple-book-recommender/
├── api.py              # FastAPI application
├── core.py             # Core logic (embeddings, Qdrant)
├── books.csv           # Dataset (not in git)
├── embeddings.npy      # Cached embeddings (not in git)
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── QDRANT.md           # Vector database documentation
└── requirements.txt    # Python dependencies
```

## 🎨 Advanced Features

### Skip Same Author

Filter out books by the same author:

```json
{
  "title_substring": "Pride and Prejudice",
  "skip_same_author": true
}
```

### Adjust Result Count

Get more or fewer recommendations:

```json
{
  "title_substring": "The Hobbit",
  "top_k": 15
}
```

## 🐛 Troubleshooting

### Qdrant Connection Error

**Error**: `Connection refused` or `401 Unauthorized`

**Solution**:
- Check if Qdrant Docker container is running: `docker ps`
- Verify API key in `core.py` matches Docker environment variable
- Use `http://localhost:6333` not `https://`

### Embeddings Taking Too Long

**Issue**: First run generates embeddings for 266k books

**Solution**:
- This happens only once (~30 minutes)
- Embeddings are cached in `embeddings.npy`
- Subsequent runs load in seconds

### Import Error: `cannot import name 'collection_name'`

**Solution**:
- `COLLECTION_NAME` is defined directly in `api.py`
- Make sure both `api.py` and `core.py` are up to date

### Git Push Failed (HTTP 408)

**Issue**: Large files (embeddings, CSV) timing out

**Solution**:
- Make sure `.gitignore` excludes large files
- Use Git LFS for large datasets if needed
- Or host data files externally (S3, Google Drive)

## 🚀 Future Enhancements

- [ ] Add collaborative filtering using user ratings
- [ ] Implement hybrid recommendations
- [ ] Add book cover image search
- [ ] Create web UI (React/Vue)
- [ ] Deploy to cloud (AWS/GCP)
- [ ] Add genre/category filtering
- [ ] Support multiple languages
- [ ] Add user feedback loop
- [ ] Implement A/B testing

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Abdelbar**
- GitHub: [@abdelbar472](https://github.com/abdelbar472)

## 🙏 Acknowledgments

- **Book-Crossing Dataset**: For providing the book data
- **Qdrant**: For the excellent vector database
- **Sentence Transformers**: For state-of-the-art embeddings
- **FastAPI**: For the modern Python web framework

## 📚 Learn More

- [What are Vector Databases?](./QDRANT.md)
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

