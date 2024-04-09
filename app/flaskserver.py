from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Function to read the Excel dataset
def read_dataset(file_path):
    try:
        return pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Failed to read the dataset: {e}")
        return None

# API endpoint to process data
@app.route('/process_data', methods=['POST'])
def process_data():
    file_path = request.json['file_path']
    df = read_dataset(file_path)
    if df is not None:
        insights = f"The dataset contains {len(df)} entries."
        # Generate more insights as needed
        return jsonify({'insights': insights}), 200
    else:
        return jsonify({'error': 'Failed to read the dataset.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
