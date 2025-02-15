from flask import Flask, request, send_file, jsonify
import pdfplumber
import pandas as pd
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file.save(file.filename)

    return send_file(file.filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
