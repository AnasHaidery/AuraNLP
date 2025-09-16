from transformers import pipeline

# Load 3-class sentiment model
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment",
    tokenizer="cardiffnlp/twitter-roberta-base-sentiment"
)

def analyze_sentiment(text: str):
    result = sentiment_analyzer(text)[0]
    label = result['label']
    score = float(result['score'])

    if label == "LABEL_0":   # Negative
        return "NEGATIVE", score
    elif label == "LABEL_2": # Positive
        return "POSITIVE", score
    else:  # Neutral → split into Positive or Negative
        if score >= 0.6:
            return "POSITIVE", score
        else:
            return "NEGATIVE", score
