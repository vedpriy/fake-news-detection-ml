import sys
import joblib
import re

model = joblib.load("fake_news_svm_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


news = sys.argv[1]

news = clean_text(news)

news_tfidf = vectorizer.transform([news])

prediction = model.predict(news_tfidf)

if prediction[0] == 0:
    print("Fake News")
else:
    print("Real News")