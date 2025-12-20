from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from core import client, model, books

# Define collection name here instead of importing it
COLLECTION_NAME = "books"

app = FastAPI(
    title="Book Recommendation API",
    description="Content-based book recommendations using vector similarity",
    version="1.0"
)

class RecommendRequest(BaseModel):
    title_substring: str
    top_k: int = 8
    skip_same_author: bool = False

class BookRecommendation(BaseModel):
    title: str
    authors: str
    year: int
    publisher: str
    similarity: float

class RecommendResponse(BaseModel):
    seed_book: str
    recommendations: List[BookRecommendation]

@app.get("/")
def home():
    return {"message": "Book Recommendation API is live! Visit /docs"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "books_loaded": len(books),
        "qdrant_collection": client.collection_exists(COLLECTION_NAME)
    }

@app.post("/recommend", response_model=RecommendResponse)
def recommend_books(req: RecommendRequest):
    query = req.title_substring.strip().lower()
    if not query:
        raise HTTPException(status_code=400, detail="title_substring required")

    matches = [b for b in books if query in b['title'].lower()]
    if not matches:
        raise HTTPException(status_code=404, detail=f"No book found matching '{req.title_substring}'")

    seed = matches[0]
    seed_vector = model.encode(seed['text'])

    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=seed_vector.tolist(),
        limit=req.top_k * 5
    ).points

    seen_titles = set()
    recs = []
    seed_title_low = seed['title'].lower()
    seed_author_low = seed['authors'].lower()

    for hit in hits[1:]:
        if len(recs) >= req.top_k:
            break
        p = hit.payload
        title_low = p['title'].lower()
        author_low = p['authors'].lower()

        if title_low in seen_titles or title_low == seed_title_low:
            continue
        if req.skip_same_author and author_low == seed_author_low:
            continue

        seen_titles.add(title_low)
        recs.append(BookRecommendation(
            title=p['title'],
            authors=p['authors'],
            year=p['year'],
            publisher=p['publisher'],
            similarity=round(hit.score, 4)
        ))

    if not recs:
        raise HTTPException(status_code=404, detail="No diverse recommendations found")

    return RecommendResponse(
        seed_book=f"{seed['title']} by {seed['authors']} ({seed['year']})",
        recommendations=recs
    )
