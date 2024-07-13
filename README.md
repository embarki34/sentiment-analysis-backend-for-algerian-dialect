
# Sentiment Analysis Flask API

This is a Flask application that provides a simple API for sentiment analysis of comments using a pretrained Transformer model. The application supports adding comments and retrieving all stored comments from a MySQL database.

## Features

- Predict sentiment (positive/negative) for input text.
- Add comments along with the predicted sentiment to the database.
- Retrieve all comments stored in the database.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7 or higher
- MySQL server
- Required Python packages (listed in requirements section)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/embarki34/your-repo-name.git
   cd your-repo-name
   ```

2. **Install the required packages:**

   Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

   Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your MySQL database:**

   Ensure you have a database named `master` and a table named `comments` with the following structure:

   ```sql
   CREATE TABLE comments (
       id INT AUTO_INCREMENT PRIMARY KEY,
       comment_text TEXT NOT NULL,
       commenter_name VARCHAR(255) NOT NULL,
       prediction VARCHAR(10) NOT NULL
   );
   ```

4. **Model and Tokenizer:**

   Make sure to download or train your sentiment analysis model and tokenizer and place them in the specified directories:

   - `model/saved_tokenizers/alger-ia_dziribert_sentiment`
   - `model/saved_models/alger-ia_dziribert_sentiment`

## Running the Application

Run the application using the following command:

```bash
python app.py
```

The API will be accessible at `http://localhost:5000`.

## API Endpoints

### 1. Predict Sentiment

**Endpoint:** `/predict`  
**Method:** `POST`  
**Request Body:**
```json
{
    "text": "Your text here"
}
```
**Response:**
```json
{
    "predicted_class": 1,
    "prediction_label": "positive"
}
```

### 2. Add Comment

**Endpoint:** `/add_comment`  
**Method:** `POST`  
**Request Body:**
```json
{
    "comment_text": "Your comment here",
    "commenter_name": "Your name"
}
```
**Response:**
```json
{
    "message": "Comment added successfully"
}
```

### 3. Get Comments

**Endpoint:** `/comments`  
**Method:** `GET`  
**Response:**
```json
[
    {
        "id": 1,
        "comment_text": "Your comment",
        "commenter_name": "Name",
        "prediction": "positive"
    },
    ...
]
```

## Error Handling

The API returns appropriate HTTP status codes and error messages for various failure scenarios, such as missing parameters or database connection errors.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Author

Omar
