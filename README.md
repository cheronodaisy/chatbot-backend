# Chatbot Backend
A chatbot using Retrieval-Augmented Generation (RAG) to answer questions based on CSV and PDF with economic data

## Features

- Loads data from CSV files and a PDF file related to Brazilian data (poverty, internet, and unemployment)
- Uses FAISS for creating a vector store from document embeddings
- Provides an API endpoint using Flask that accepts user input and returns responses from the chatbot
- Uses TinyBERT for question-answering
- Implements error handling for common issues

## Requirements

- Python 3.8+
- Flask
- transformers
- langchain_community
- pandas
- PyPDF2
- FAISS

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/cheronodaisy/chatbot-backend.git
    ```

2. Navigate to the project directory:
    ```bash
    cd chatbot-backend
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the Flask server:
    ```bash
    python app.py
    ```

2. The application will be running at `http://127.0.0.1:5000`.

## API Endpoints

- **POST /chatbot/**: Accepts a JSON body with a `question` field and returns a JSON response with the `answer`.

- **GET /**: Returns a simple message indicating that the API is running.

## Testing

Run the tests using:
```bash
python test_app.py
