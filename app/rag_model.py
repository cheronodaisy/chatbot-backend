from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer, pipeline
import pandas as pd
import os
import PyPDF2

class Document:
    """A simple class to represent documents with page content."""
    def __init__(self, text, metadata=None):
        self.page_content = text
        self.metadata = metadata

# Load CSV and PDF Data
def load_data():
    documents = []
    csv_files = ['data/poverty.csv', 'data/internet.csv', 'data/unemployment.csv']
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            text = str(row.values)
            documents.append(Document(text=text, metadata={"source": csv_file}))
    
    pdf_path = 'data/gem_report.pdf'
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_text = ""
        for page_num in range(len(pdf_reader.pages)):
            pdf_text += pdf_reader.pages[page_num].extract_text()
        documents.append(Document(text=pdf_text, metadata={"source": "GEM Report"}))
    
    return documents

# Document Transformers
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(load_data())

# Text Embedding
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-l6-v2",
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

# Set up Vector Stores
db = FAISS.from_documents(docs, embeddings)

# Set up retrievers
retriever = db.as_retriever(search_kwargs={"k": 4})

tokenizer = AutoTokenizer.from_pretrained("Intel/dynamic_tinybert", padding=True, truncation=True, max_length=512)

# Define a question-answering pipeline using the model and tokenizer
question_answerer = pipeline(
    "question-answering",
    model="Intel/dynamic_tinybert",
    tokenizer=tokenizer,
    return_tensors='pt'
)

# Generate response based on a question
def generate(question):
    docs = retriever.get_relevant_documents(question)
    context = docs[0].page_content
    squad_ex = question_answerer(question=question, context=context)
    return squad_ex['answer']

# Example Usage
if __name__ == "__main__":
    question = "What is the poverty headcount ratio in Brazil?"
    response = generate(question)
    print(response)