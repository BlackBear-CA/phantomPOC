from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from langchain.llms import OpenAI

app = Flask(__name__)
CORS(app, origins=['http://phantomaip.azurewebsites.net', 'https://phantomaip.azurewebsites.net'])

# Initialize LangChain with your actual OpenAI API key
# Make sure to secure your API key properly, consider using environment variables for production
llm = OpenAI(api_key="your_openai_api_key")

# Function to read Excel and CSV datasets
def read_dataset(file):
    if file.filename.endswith('.docx'):
        try:
            from docx import Document
            doc = Document(file)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            print(f'Failed to read the DOCX file: {e}')
    elif file.filename.endswith('.pdf'):
        try:
            import pdfplumber
            with pdfplumber.open(file) as pdf:
                full_text = [page.extract_text() for page in pdf.pages]
            return '\n'.join(filter(None, full_text))
        except Exception as e:
            print(f'Failed to read the PDF file: {e}')
    if file.filename.endswith('.xlsx'):
        try:
            return pd.read_excel(file, engine='openpyxl')
        except Exception as e:
            print(f"Failed to read the Excel dataset: {e}")
    elif file.filename.endswith('.csv'):
        try:
            return pd.read_csv(file)
        except Exception as e:
            print(f"Failed to read the CSV dataset: {e}")
    else:
        print("Unsupported file format.")
    return None

# Function to generate insights from the dataset
def generate_insights(df):
    insights = []
    if df is not None:
        insights.append(f"The dataset contains {len(df)} entries.")
        numerical_columns = df.select_dtypes(include='number').columns
        if not numerical_columns.empty:
            for column in numerical_columns:
                insights.append(f"The average of {column} is {df[column].mean():.2f}.")
        else:
            insights.append("There are no numerical columns to summarize.")
    return " ".join(insights)

# Function to generate casual conversation about the dataset using LangChain
def casual_chat_about_data(insights):
    prompt = f"Based on the data analysis, here's what I found: {insights} Can we delve into something specific?"
    try:
        response = llm.generate(prompt=prompt, max_tokens=100)
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"LangChain error: {e}")
        return "I encountered an error while generating a response."

# API endpoint to process and chat about data
@app.route('/process_data', methods=['POST'])
def process_data():
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected or file is empty.'}), 400
    df = read_dataset(file)
    if df is not None:
        insights = generate_insights(df)
        conversation = casual_chat_about_data(insights)
        return jsonify({'insights': insights, 'conversation': conversation}), 200
    else:
        return jsonify({'error': 'Failed to read the dataset or unsupported format.'}), 400

# Root URL route
@app.route('/')
def index():
    return 'Welcome to the Flask backend API!'

if __name__ == '__main__':
    app.run(debug=True)
