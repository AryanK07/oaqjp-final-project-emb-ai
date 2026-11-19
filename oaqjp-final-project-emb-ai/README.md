# Final project

## Emotion Detector

A Flask web application that submits English text to the IBM Watson NLP EmotionPredict endpoint. It shows the scores for anger, disgust, fear, joy, and sadness, as well as the highest-scoring emotion.

### Start the application

From the project root, preferably in the IBM Skills Network lab:

```bash
python3 -m pip install -r requirements-dev.txt
python3 server.py
```

Open `http://127.0.0.1:5000` locally. In a remote lab, run `HOST=0.0.0.0 python3 server.py` and use the lab's port 5000 preview. The default Watson URL points to the course service. `WATSON_EMOTION_URL` can override it if the lab supplies a different endpoint.

### Tests and static analysis

```bash
python3 -m unittest -v test_emotion_detection
python3 -m pylint server.py
```

The five classification unit tests mock the network response by default. With live Watson access, use `WATSON_LIVE_TESTS=1 python3 -m unittest -v test_emotion_detection` to exercise those same cases against the service. Local blank-input and simulated HTTP 400 tests run in both modes.

### Flask endpoint

`GET /emotionDetector?textToAnalyze=...` returns the five scores and the dominant emotion. A blank input or a Watson HTTP 400 returns `Invalid text! Please try again!` with HTTP 400. An unavailable or malformed upstream response returns HTTP 503.

Starter repository: [IBM Skills Network](https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai).
