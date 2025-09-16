import random
from flask import Flask, render_template, request, jsonify
from modules.nlp_utils import preprocess_text, summarize_text, correct_spelling
from modules.sentiment import analyze_sentiment
from modules.context import ContextManager

# 🔹 Create Flask app instance
app = Flask(__name__)
context_manager = ContextManager()

# Predefined Q&A with variations
qa_pairs = {
    ("hello", "hi", "hey", "heyy", "hey there", "yo", "hiya"):
        "Hello! I’m AURA ✨, your study buddy.",

    ("exam", "exams", "test", "when is my exam", "exam date", "next exam", "got exams coming up?"):
        "Your next exam is scheduled on 25th September.",

    ("deadline", "last date", "submission date", "when to submit", "project deadline"):
        "The project submission deadline is 30th September.",

    ("library", "reading room", "study hall", "where is the library", "library timings"):
        "The library is open from 8 AM to 10 PM daily.",

    ("schedule", "class timing", "timetable", "subjects tomorrow", "when is my class"):
        "You have Math at 9 AM and Physics at 11 AM tomorrow.",

    ("assignment", "homework", "task", "submit assignment", "any pending work?"):
        "Don’t forget, your assignment is due this Friday.",

    ("motivate", "motivation", "encourage me", "say something positive", "cheer me up"):
        "You are capable of amazing things. Keep going 💪!",

    ("holiday", "vacation", "holiday date", "next holiday", "when is the holiday?"):
        "The next holiday is on 2nd October (Gandhi Jayanti).",

    ("fees", "payment", "last date for fees", "pay fees", "fee deadline"):
        "The last date to pay fees is 15th October.",

    ("bye", "goodbye", "see you", "later", "catch you later"):
        "Goodbye 👋! Come back whenever you need me.",
}

# Sentiment-based responses
negative_responses = [
    "I sense stress 😟. Take a deep breath—you’ll get through this!",
    "It sounds tough 💔. Do you want me to suggest a relaxation exercise?",
    "I hear you. It’s okay to feel low sometimes 🌧️.",
    "That seems overwhelming 😞. Maybe take a short walk?",
    "Don’t be too hard on yourself ❤️. You’re doing your best.",
    "I know it feels difficult now, but brighter days are ahead 🌅.",
]

positive_responses = [
    "That’s awesome! Keep up the great work 🎉.",
    "I love your energy ✨. Stay positive!",
    "You’re on the right track 🚀.",
    "That makes me happy to hear 😃.",
    "Amazing! Keep shining 🌟.",
]

# 🔹 Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_msg = request.json["message"]

    # Step 1: Correct spelling
    corrected_msg = correct_spelling(user_msg)
    print(f"DEBUG: Original='{user_msg}' | Corrected='{corrected_msg}'")

    # Step 2: Sentiment analysis
    sentiment, score = analyze_sentiment(corrected_msg)
    print(f"DEBUG: Sentiment={sentiment}, Score={score:.3f}")

    # Default response
    bot_msg = None

    # Step 3: Summarization
    tokens = preprocess_text(corrected_msg.lower())
    if "summarize" in tokens:
        bot_msg = summarize_text(corrected_msg)
    else:
        for keys, answer in qa_pairs.items():
            if any(k in corrected_msg.lower() for k in keys):
                bot_msg = answer
                break

    # Step 4: Sentiment-driven fallback
    if not bot_msg:
        if sentiment == "NEGATIVE":
            bot_msg = random.choice(negative_responses)
        elif sentiment == "POSITIVE":
            bot_msg = random.choice(positive_responses)

    # Save conversation history (store original input for realism)
    context_manager.add_message(user_msg, bot_msg)

    return jsonify({"reply": bot_msg, "sentiment": sentiment})

if __name__ == "__main__":
    app.run(debug=True)
