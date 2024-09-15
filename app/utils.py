import requests
import fitz  # PyMuPDF
import pandas as pd
import zipfile 
import os

def fetch_data():
    # URLs for the CSV data
    data_urls = {
        'poverty': 'https://api.worldbank.org/v2/en/indicator/SI.POV.DDAY?downloadformat=csv',
        'internet': 'https://api.worldbank.org/v2/en/indicator/IT.NET.USER.ZS?downloadformat=csv',
        'unemployment': 'https://api.worldbank.org/v2/en/indicator/SL.UEM.TOTL.ZS?downloadformat=csv'
    }

    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Download and process CSV data
    for name, url in data_urls.items():
        response = requests.get(url)
        zip_filename = f'data/{name}.zip'
        
        with open(zip_filename, 'wb') as f:
            f.write(response.content)

        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(f'data/{name}')
        
        extracted_files = [f for f in os.listdir(f'data/{name}') if f.endswith('.csv')]
        main_csv = max(extracted_files, key=lambda x: os.path.getsize(f'data/{name}/{x}'))
        
        df = pd.read_csv(f'data/{name}/{main_csv}', skiprows=4)
        output_csv_filename = f'data/{name}.csv'
        df.to_csv(output_csv_filename, index=False)

def extract_pdf_data(pdf_url, output_txt_file):
    response = requests.get(pdf_url)
    pdf_filename = os.path.join('data', 'gem_report.pdf')
    with open(pdf_filename, 'wb') as f:
        f.write(response.content)
    doc = fitz.open(pdf_filename)
    text = ''
    for page in doc:
        text += page.get_text()
    with open(output_txt_file, 'w') as txt_file:
        txt_file.write(text)
    return text

# Example of usage
if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
    
    fetch_data()
    gem_pdf_url = 'https://gemconsortium.org/file/open?fileId=51377' 
    extract_pdf_data(gem_pdf_url, os.path.join('data', 'gem_report.txt'))
