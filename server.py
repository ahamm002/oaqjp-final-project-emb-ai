"""Flask server for use with the emotion detection functionality."""

import json

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector




app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def sent_detector():
    """
    Analyzes text provided in the request args using emotion_detector function.
    Returns formatted string of emotion scores and dominant emotion.
    """
    text_to_analyze = request.args.get("textToAnalyze")

    response_text = emotion_detector(text_to_analyze)
    response = json.loads(response_text)

    if response.get("dominant_emotion") is None:
        return "Invalid text! Please try again!"

    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, 'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


@app.route("/")
def render_index_page():
    """Renders the index.html page for the Flask app."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
