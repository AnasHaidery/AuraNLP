import spacy
from transformers import pipeline
from spellchecker import SpellChecker

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Initialize spell checker
spell = SpellChecker()

def preprocess_text(text):
    """Tokenize and lemmatize text with spaCy, removing stopwords and non-alpha tokens."""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return tokens

def summarize_text(text):
    """Generate abstractive summary using BART if text is long enough."""
    if len(text.split()) < 30:
        return "Text too short to summarize."
    summary = summarizer(text, max_length=60, min_length=20, do_sample=False)
    return summary[0]['summary_text']

def correct_spelling(text: str) -> str:
    """Correct spelling mistakes using pyspellchecker."""
    words = text.split()
    corrected_words = [spell.correction(word) or word for word in words]
    return " ".join(corrected_words)
