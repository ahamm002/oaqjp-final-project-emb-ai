import json
import unittest
from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Unit tests for the emotion_detector function."""

    def _assert_dominant_emotion(self, text, expected_emotion):
        """Helper to invoke emotion_detector and assert dominant_emotion."""
        raw_result = emotion_detector(text)
        response = json.loads(raw_result)
        self.assertEqual(response["dominant_emotion"], expected_emotion)

    def test_joy(self):
        """Verify dominant emotion is joy."""
        self._assert_dominant_emotion("I am glad this happened", "joy")

    def test_anger(self):
        """Verify dominant emotion is anger."""
        self._assert_dominant_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        """Verify dominant emotion is disgust."""
        self._assert_dominant_emotion(
            "I feel disgusted just hearing about this", "disgust"
        )

    def test_sadness(self):
        """Verify dominant emotion is sadness."""
        self._assert_dominant_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        """Verify dominant emotion is fear."""
        self._assert_dominant_emotion(
            "I am really afraid that this will happen", "fear"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)