"""Test the five emotion classes and invalid input handling."""

import os
import unittest
from unittest.mock import patch

import requests

from EmotionDetection import EMOTIONS, emotion_detector


class EmotionDetectorTests(unittest.TestCase):
    """Run mocked unit tests, or live classification checks when requested."""

    def check_emotion(self, text, expected):
        """Assert the output schema and the expected dominant emotion."""
        if os.getenv("WATSON_LIVE_TESTS") == "1":
            result = emotion_detector(text)
        else:
            scores = dict.fromkeys(EMOTIONS, 0.04)
            scores[expected] = 0.84
            with patch("EmotionDetection.emotion_detection.requests.post") as post:
                post.return_value.status_code = 200
                post.return_value.json.return_value = {
                    "emotionPredictions": [{"emotion": scores}]
                }
                result = emotion_detector(text)
                post.assert_called_once()
                self.assertEqual(post.call_args.kwargs["json"], {"raw_document": {"text": text}})

        self.assertEqual(set(result), {*EMOTIONS, "dominant_emotion"})
        self.assertEqual(result["dominant_emotion"], expected)

    def test_joy(self):
        """Recognize the joy case."""
        self.check_emotion("I am glad this happened", "joy")

    def test_anger(self):
        """Recognize the anger case."""
        self.check_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        """Recognize the disgust case."""
        self.check_emotion("I feel disgusted just hearing about this", "disgust")

    def test_sadness(self):
        """Recognize the sadness case."""
        self.check_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        """Recognize the fear case."""
        self.check_emotion("I am really afraid that this will happen", "fear")

    def test_blank_input(self):
        """Return an invalid result without calling the service."""
        with patch("EmotionDetection.emotion_detection.requests.post") as post:
            self.assertEqual(emotion_detector("   "), dict.fromkeys((*EMOTIONS, "dominant_emotion")))
            post.assert_not_called()

    def test_watson_http_400(self):
        """Translate a Watson 400 response to the invalid result schema."""
        response = requests.Response()
        response.status_code = 400
        with patch("EmotionDetection.emotion_detection.requests.post", return_value=response):
            self.assertEqual(emotion_detector("Some input"), dict.fromkeys((*EMOTIONS, "dominant_emotion")))


if __name__ == "__main__":
    unittest.main()
