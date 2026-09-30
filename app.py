from flask import Flask, request, jsonify
import joblib
import re
import os

app = Flask(__name__)


# -----------------------------
# CORS
# -----------------------------
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


# -----------------------------
# Load Model
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(
    os.path.join(BASE_DIR, "fake_news_svm_model.pkl")
)

vectorizer = joblib.load(
    os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")
)


# -----------------------------
# Text Cleaning
# -----------------------------
def clean_text(text):
    text = text.lower()

    text = re.sub(
        r"http\S+|www\S+|https\S+",
        "",
        text
    )

    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():
    return "Fake News Detection API is running!"


# -----------------------------
# Prediction
# -----------------------------
@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():

    # Handle browser CORS preflight
    if request.method == "OPTIONS":
        return "", 204

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


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )