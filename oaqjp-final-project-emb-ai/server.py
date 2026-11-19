"""Serve the Emotion Detector page and its Watson-powered Flask endpoint."""

import os

from flask import Flask, render_template, request

from EmotionDetection import EMOTIONS, WatsonServiceError, emotion_detector

app = Flask(__name__)
INVALID_TEXT = "Invalid text! Please try again!"


@app.get("/")
def index():
    """Render the browser interface."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion():
    """Analyze text and return the five scores and the dominant emotion."""
    text_to_analyze = request.args.get("textToAnalyze", "").strip()
    if not text_to_analyze:
        return INVALID_TEXT, 400

    try:
        result = emotion_detector(text_to_analyze)
    except WatsonServiceError:
        return "Watson NLP is unavailable. Please try again later.", 503

    if result["dominant_emotion"] is None:
        return INVALID_TEXT, 400

    scores = ", ".join(f"'{name}': {result[name]}" for name in EMOTIONS)
    return (
        f"For the given statement, the system response is {scores}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
    )
