"""Call IBM Watson NLP and format its emotion predictions."""

import math
import os

import requests

DEFAULT_ENDPOINT = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL = "emotion_aggregated-workflow_lang_en_stock"
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


class WatsonServiceError(RuntimeError):
    """Watson could not return a usable prediction."""


def invalid_result():
    """Return the output schema with all fields set to None."""
    return dict.fromkeys((*EMOTIONS, "dominant_emotion"))


def emotion_detector(text_to_analyze):
    """Return five Watson scores and the highest-scoring emotion."""
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return invalid_result()

    url = os.getenv("WATSON_EMOTION_URL") or DEFAULT_ENDPOINT
    header = {"grpc-metadata-mm-model-id": MODEL}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(url, json=payload, headers=header, timeout=12)
        if response.status_code == 400:
            return invalid_result()
        response.raise_for_status()
    except requests.RequestException as error:
        raise WatsonServiceError("The Watson request failed.") from error

    try:
        prediction = response.json()["emotionPredictions"][0]["emotion"]
        scores = {name: float(prediction[name]) for name in EMOTIONS}
        if not all(math.isfinite(score) and 0 <= score <= 1 for score in scores.values()):
            raise ValueError("Emotion scores must be finite numbers from zero to one.")
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise WatsonServiceError("Watson returned an invalid prediction.") from error

    return {**scores, "dominant_emotion": max(scores, key=scores.__getitem__)}
