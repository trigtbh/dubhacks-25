from google import genai
from google.genai import types
from app.config import settings
from typing import List

client = genai.Client(api_key=settings.gemini_api_key)

def embed_content(content: str):
    return client.models.embed_content(
        model="gemini-embedding-001",
        contents=content,
        config=types.EmbedContentConfig(output_dimensionality=768)
    ).embeddings[0].values

def dist(vec1: List[float], vec2: List[float]) -> float:
    return sum((x - y)**2 for x,y in zip(vec1, vec2)) ** 0.5

personas = [
    ["The Coffeehouse Creator", "I’m the kind of person who brings a sketchpad everywhere. I love designing interfaces, doodling random characters, and finding hidden-gem coffee shops with chill playlists. Most nights, you’ll catch me working late with lo-fi beats and a cortado. I get inspired by aesthetics, indie games, and conversations that turn into creative projects."],
    ["The Outdoors Hacker", "When I’m not coding, I’m hiking, rock climbing, or planning my next camping trip. I love solving problems that connect tech and the environment — solar energy, mapping trails, or anything sustainability-related. My best ideas always come when I’m halfway up a mountain or sitting by a campfire with friends."],
    ["The Chill Gamer", "I’m a night owl who loves winding down with co-op games and anime marathons. I’m easygoing, love meme humor, and tend to make spontaneous side projects just for fun. Hackathons are my way of meeting like-minded folks who don’t take themselves too seriously but still build cool stuff."],
    ["The Social Catalyst", "I’m here mostly for the people — I get energy from talking ideas into existence. Whether it’s hosting game nights, organizing brainstorms, or making sure everyone gets a voice, I thrive on collaboration. Outside of hackathons, I’m usually at concerts, trivia nights, or exploring new restaurants with friends."],
    ["The Deep Thinker", "I’m into philosophy, psychology, and quiet spaces where ideas can unfold. I love long walks with podcasts, journaling, and working on projects that explore human behavior or emotion. I tend to dive deep into whatever I’m learning and love discussions that challenge assumptions."],
    ["The Fitness Futurist", "I’m obsessed with self-improvement — tracking workouts, optimizing routines, and experimenting with biohacking tools. My weekends are a mix of trail runs, gym sessions, and reading about nutrition or longevity science. I like building projects that make people healthier or more mindful."],
    ["The Global Nomad", "I’ve been traveling for years, working from different cities, and collecting stories from everywhere I go. I love meeting people from different backgrounds, trying new foods, and photographing street life. My favorite hackathon projects usually solve real-world problems with an international twist."],
    ["The Music Maker", "Music runs everything for me — I produce beats, go to small shows, and DJ for fun when I can. I love anything with rhythm, from coding flow sessions to late-night jam circles. If we work together, expect a curated playlist and spontaneous dance breaks."],
    ["The Cozy Coder", "I’m all about cozy vibes — blankets, tea, and a playlist of movie scores while I code. I love small creative projects, story-driven games, and slow mornings with good books. My ideal hackathon team feels like a mini family where everyone supports each other."],
    ["The Builder Dreamer", "I get hooked on ideas that feel a little bit impossible. I love tinkering with prototypes, starting side hustles, and learning by doing. When I’m not working on something new, I’m watching documentaries about inventors or sketching wild product ideas. I’m equal parts idealist and hands-on maker."]
]

embeddings = [embed_content(c) for n, c in personas]

import json
with open("personas.json", "w") as f:
    json.dump(embeddings, f)

def classify(content: str) -> int:
    user = embed_content(content)
    return min(((i, dist(user, e)) for i, e in enumerate(embeddings)), key=lambda x: x[1])[0]

print("You are:", personas[classify(input("> "))][0])
