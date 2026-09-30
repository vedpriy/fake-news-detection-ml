from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import os

app = Flask(__name__)

# Allow requests from the deployed frontend
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(
    os.path.join(BASE_DIR, "fake_news_svm_model.pkl")
)

vectorizer = joblib.load(
    os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")
)


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


@app.route("/")
def home():
    return "Fake News Detection API is running!"


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    news = data.get("news", "")

    if not news:
        return jsonify({
            "error": "News text is required"
        }), 400

    news = clean_text(news)

    news_tfidf = vectorizer.transform([news])

    prediction = model.predict(news_tfidf)

    if prediction[0] == 0:
        result = "Fake News"
    else:
        result = "Real News"

    return jsonify({
        "prediction": result
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )