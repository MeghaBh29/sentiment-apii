from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class SentimentRequest(BaseModel):
    sentences: List[str]

class SentimentResult(BaseModel):
    sentence: str
    sentiment: str

class SentimentResponse(BaseModel):
    results: List[SentimentResult]

def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower()

    happy_words = [
        "love", "great", "amazing", "awesome", "happy", "excellent",
        "fantastic", "wonderful", "good", "best", "joy", "excited",
        "glad", "beautiful", "perfect", "brilliant", "superb", "enjoy",
        "pleased", "delighted", "fun", "nice", "incredible", "grateful",
        "thankful", "thrilled", "cheerful", "positive", "hope", "win",
        "success", "laugh", "smile", "favorite"
    ]

    sad_words = [
        "terrible", "horrible", "awful", "hate", "sad", "bad", "worst",
        "disappointing", "disgusting", "useless", "angry", "upset",
        "depressed", "miserable", "frustrated", "annoying", "broken",
        "failed", "failure", "cry", "pain", "hurt", "regret", "sorry",
        "unfortunate", "poor", "waste", "disaster", "problem", "wrong",
        "dislike", "boring", "dreadful", "unfair", "suffer"
    ]

    happy_count = sum(1 for word in happy_words if word in text)
    sad_count = sum(1 for word in sad_words if word in text)

    if happy_count > sad_count:
        return "happy"
    elif sad_count > happy_count:
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment", response_model=SentimentResponse)
def sentiment_analysis(request: SentimentRequest):
    results = []
    for sentence in request.sentences:
        sentiment = analyze_sentiment(sentence)
        results.append(SentimentResult(sentence=sentence, sentiment=sentiment))
    return SentimentResponse(results=results)
