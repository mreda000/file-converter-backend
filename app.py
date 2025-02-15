from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import subprocess

# Initialize Flask App
app = Flask(__name__)

# Enable CORS to allow frontend requests
CORS(app, resources={r"/*": {"origins": "*"}})

# Set up upload folder
UPLOAD_FOLDER = "/tmp"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():
    return "Welcome to the File Converter API! Use /upload to upload a file."

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save input file
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(input_path)

    # Determine output file name
    output_filename = os.path.splitext(file.filename)[0] + ".docx"
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_filename)

    # Convert PDF to Word using LibreOffice
    try:
        conversion_command = [
            "libreoffice",
            "--headless",
            "--convert-to",
            "docx",
            "--outdir",
            UPLOAD_FOLDER,
            input_path,
        ]

        subprocess.run(conversion_command, check=True)

        if not os.path.exists(output_path):
            return jsonify({"error": "Converted file not found"}), 500

        return send_file(output_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
