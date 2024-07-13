from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pymysql.cursors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # replace with your MySQL root password
    'database': 'master',
    'cursorclass': pymysql.cursors.DictCursor
}

# Load the tokenizer and model
tokenizer_dir = "model/saved_tokenizers/alger-ia_dziribert_sentiment"
model_dir = "model/saved_models/alger-ia_dziribert_sentiment"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
print("Loading model...")
model = AutoModelForSequenceClassification.from_pretrained(model_dir)

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    predicted_class = predict_sentiment(text)
    prediction_label = 'positive' if predicted_class == 1 else 'negative'
    return jsonify({"predicted_class": predicted_class, "prediction_label": prediction_label})

@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.json
    comment_text = data.get('comment_text')
    commenter_name = data.get('commenter_name')

    if not comment_text or not commenter_name:
        return jsonify({"error": "comment_text and commenter_name are required"}), 400

    predicted_class = predict_sentiment(comment_text)
    prediction_label = 'positive' if predicted_class == 1 else 'negative'

    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            sql = "INSERT INTO comments (comment_text, commenter_name, prediction) VALUES (%s, %s, %s)"
            cursor.execute(sql, (comment_text, commenter_name, prediction_label))
        connection.commit()
        return jsonify({"message": "Comment added successfully"}), 201
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/comments', methods=['GET'])
def get_comments():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM comments")
            comments = cursor.fetchall()
        return jsonify(comments)
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
