
from flask import Flask, request, jsonify
import pandas as pd
from langchain.llms import OpenAI

app = Flask(__name__)

# Initialize LangChain with your actual OpenAI API key
llm = OpenAI(api_key="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")

# Function to read the Excel dataset
def read_dataset(file):
    try:
        # Using 'openpyxl' as the engine for reading .xlsx files
        return pd.read_excel(file, engine='openpyxl')
    except Exception as e:
        print(f"Failed to read the dataset: {e}")
        return None

# Function to generate insights from the dataset
def generate_insights(df):
    insights = []
    if df is not None:
        # Generating basic insights
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
        # Correctly invoking the generate method of LangChain's LLM
        response = llm.generate(prompt)
        # Parsing the response correctly based on the LangChain response structure
        return response.get("choices")[0].get("text").strip()
    except Exception as e:
        print(f"LangChain error: {e}")
        return "I encountered an error while generating a response."

# API endpoint to process data
@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected.'}), 400
        df = read_dataset(file)
        if df is not None:
            insights = generate_insights(df)
            conversation = casual_chat_about_data(insights)
            return jsonify({'insights': insights, 'conversation': conversation}), 200
        else:
            return jsonify({'error': 'Failed to read the dataset.'}), 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing the data.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import pandas as pd
from langchain.llms import OpenAI

app = Flask(__name__)

# Initialize LangChain with your actual OpenAI API key
llm = OpenAI(api_key="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")

# Function to read the Excel dataset
def read_dataset(file):
    try:
        # Using 'openpyxl' as the engine for reading .xlsx files
        return pd.read_excel(file, engine='openpyxl')
    except Exception as e:
        print(f"Failed to read the dataset: {e}")
        return None

# Function to generate insights from the dataset
def generate_insights(df):
    insights = []
    if df is not None:
        # Generating basic insights
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
        # Correctly invoking the generate method of LangChain's LLM
        response = llm.generate(prompt)
        # Parsing the response correctly based on the LangChain response structure
        return response.get("choices")[0].get("text").strip()
    except Exception as e:
        print(f"LangChain error: {e}")
        return "I encountered an error while generating a response."

# API endpoint to process data
@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected.'}), 400
        df = read_dataset(file)
        if df is not None:
            insights = generate_insights(df)
            conversation = casual_chat_about_data(insights)
            return jsonify({'insights': insights, 'conversation': conversation}), 200
        else:
            return jsonify({'error': 'Failed to read the dataset.'}), 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing the data.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

