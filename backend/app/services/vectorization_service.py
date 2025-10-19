from google import genai
from google.genai import types
from app.config import settings
from typing import List, Set
import json

client = genai.Client(api_key=settings.gemini_api_key)

def embed_content(content: str) -> List[float]:
    return client.models.embed_content(
        model="gemini-embedding-001",
        contents=content,
        config=types.EmbedContentConfig(output_dimensionality=768)
    ).embeddings[0].values

def dist(vec1: List[float], vec2: List[float]) -> float:
    return sum((x - y)**2 for x,y in zip(vec1, vec2)) ** 0.5

with open("personas.json", "r") as f:
    embeddings = json.load(f)

def classify(content: str, visited: Set[int]) -> int:
    user = embed_content(content)
    return min(((i, dist(user, e)) for i, e in enumerate(embeddings) if not i in visited), key=lambda x: x[1])[0]
