from flask import Flask, request, jsonify, send_file
import pdfplumber
import pandas as pd
import os

# 🔹 Define Flask app FIRST before any route
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the File Converter API! Use /upload to upload a file."

UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    output_path = process_conversion(file_path)
    return send_file(output_path, as_attachment=True)

def process_conversion(file_path):
    output_file = file_path.replace(".pdf", ".xlsx")
    with pdfplumber.open(file_path) as pdf:
        tables = []
        for page in pdf.pages:
            extracted_table = page.extract_table()
            if extracted_table:
                tables.append(pd.DataFrame(extracted_table))
        if tables:
            final_df = pd.concat(tables, ignore_index=True)
            final_df.to_excel(output_file, index=False)
    return output_file

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)


