import json
import sys
import requests


def emotion_detector(text_to_analyse):
    """
    Analyzes the emotion in a given text using the Watson Emotion Prediction API
    and returns a JSON string containing individual emotion scores and the
    dominant emotion (or None values if status 400 is returned).
    """
    URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    HEADERS = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    INPUT_JSON = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(URL, json=INPUT_JSON, headers=HEADERS)

        # 1. Handle Status Code 400 (Blank/Invalid Input)
        if response.status_code == 400:
            return json.dumps(
                {
                    "anger": None,
                    "disgust": None,
                    "fear": None,
                    "joy": None,
                    "sadness": None,
                    "dominant_emotion": None,
                }
            )

        # 2. Parse the successful response (Status 200)
        response_json = json.loads(response.text)

        # Extract the scores
        emotions = response_json["emotionPredictions"][0]["emotion"]

        # Determine the dominant emotion
        dominant_emotion = max(emotions, key=emotions.get)

        # 3. Return the populated dictionary as a JSON string
        final_dictionary = {
            "anger": emotions["anger"],
            "disgust": emotions["disgust"],
            "fear": emotions["fear"],
            "joy": emotions["joy"],
            "sadness": emotions["sadness"],
            "dominant_emotion": dominant_emotion,
        }
        return json.dumps(final_dictionary)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        return json.dumps(
            {
                "error": str(e),
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            }
        )


# ------------------------------------------------------------------------------
## Main Execution Block (Optional CLI runner)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    text = input("Please input your text for emotion analysis: ")

    if not text.strip():
        print("\nInput cannot be empty. Please try again.")
        sys.exit()

    json_output_string = emotion_detector(text)

    if json_output_string:
        try:
            final_result_dict = json.loads(json_output_string)

            if final_result_dict.get("error"):
                print("\nFunction returned an error message:")
                print(f"Details: {final_result_dict.get('error')}")
                if "status_code" in final_result_dict:
                    print(f"Status Code: {final_result_dict['status_code']}")
                sys.exit()

            if final_result_dict.get("dominant_emotion") is None:
                print("\nInvalid text! Please try again.")
                sys.exit()

            print(f"\nEmotion Analysis Success for: '{text}'")
            print("---------------------------------")

            for emotion in ["anger", "disgust", "fear", "joy", "sadness"]:
                print(
                    f"| {emotion.ljust(6)} | Score: {final_result_dict[emotion]:.4f} |"
                )

            print(
                f"| Dominant Emotion: {final_result_dict['dominant_emotion'].upper()} |"
            )
            print("---------------------------------")

        except json.JSONDecodeError as e:
            print(
                f"\nError processing JSON output: Could not decode the string into a dictionary: {e}"
            )
            print("Raw Output String:", json_output_string)