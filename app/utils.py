import requests
import fitz  # PyMuPDF
import pandas as pd
import zipfile 
import os

def fetch_data(data_urls, data_dir='data'):
    """
    Downloads zip files from given URLs, extracts CSV files, 
    and saves the largest CSV file as a single CSV file in the specified directory.
    """
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)

    for name, url in data_urls.items():
        zip_filename = os.path.join(data_dir, f'{name}.zip')
        
        # Download zip file
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for unsuccessful requests
        with open(zip_filename, 'wb') as f:
            f.write(response.content)

        # Extract zip file
        extract_dir = os.path.join(data_dir, name)
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find the largest CSV file
        extracted_files = [f for f in os.listdir(extract_dir) if f.endswith('.csv')]
        if extracted_files:
            main_csv = max(extracted_files, key=lambda x: os.path.getsize(os.path.join(extract_dir, x)))
            df = pd.read_csv(os.path.join(extract_dir, main_csv), skiprows=4)
            output_csv_filename = os.path.join(data_dir, f'{name}.csv')
            df.to_csv(output_csv_filename, index=False)
        else:
            print(f"No CSV files found in {extract_dir}")

def extract_pdf_data(pdf_url, output_txt_file, data_dir='data'):
    """
    Downloads a PDF file from a given URL, extracts its text, 
    and saves the text to a specified file.
    """
    response = requests.get(pdf_url)
    response.raise_for_status()  # Raise an error for unsuccessful requests

    pdf_filename = os.path.join(data_dir, 'gem_report.pdf')
    with open(pdf_filename, 'wb') as f:
        f.write(response.content)
    
    # Extract text from PDF
    doc = fitz.open(pdf_filename)
    text = ''.join(page.get_text() for page in doc)
    with open(output_txt_file, 'w') as txt_file:
        txt_file.write(text)
    
    return text

# Example of usage
if __name__ == "__main__":
    data_urls = {
        'poverty': 'https://api.worldbank.org/v2/en/indicator/SI.POV.DDAY?downloadformat=csv',
        'internet': 'https://api.worldbank.org/v2/en/indicator/IT.NET.USER.ZS?downloadformat=csv',
        'unemployment': 'https://api.worldbank.org/v2/en/indicator/SL.UEM.TOTL.ZS?downloadformat=csv'
    }
    
    fetch_data(data_urls)
    gem_pdf_url = 'https://gemconsortium.org/file/open?fileId=51377' 
    extract_pdf_data(gem_pdf_url, os.path.join('data', 'gem_report.txt'))
