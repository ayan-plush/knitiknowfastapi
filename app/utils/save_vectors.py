from pymongo import MongoClient
import os
from app.utils.vectorizer import vectorize_article

client = MongoClient(os.getenv("MONGO_URI"))
vector_collection = client["neta"]["loksabhaRAGChunks"]

def save_vectorized_article(article_dict):
    mp_name = article_dict["politicianName"]
    mp_id = article_dict["politician"]["$oid"]
    chunks = vectorize_article(article_dict["text"], mp_name)

    for chunk, embedding in chunks:
        vector_collection.insert_one({
            "mpId": mp_id,
            "mpName": mp_name,
            "chunk": chunk,
            "embedding": embedding,
            "metadata": {
                "articleUrl": article_dict["url"],
                "title": article_dict["title"],
                "scrapedAt": article_dict["scrapedAt"],
                "scrapedAt": article_dict["description"],
                "type": "general"
            }
        })
