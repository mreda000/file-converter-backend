from flask import Flask, request, send_file
from flask_cors import CORS  # Import CORS
import os

# Initialize Flask App
app = Flask(__name__)
CORS(app, origins=["https://scintillating-stroopwafel-85feb2.netlify.app"])  # Allow frontend

# Configure Upload Folder
UPLOAD_FOLDER = "/tmp/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return "Welcome to the File Converter API! Use /upload to upload a file."

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files["file"]
    if file.filename == "":
        return {"error": "No selected file"}, 400

    # Save input file
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(input_path)

    # Generate output filename
    output_filename = file.filename.rsplit(".", 1)[0] + ".docx"
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_filename)

    # Convert PDF to Word using LibreOffice
    try:
        os.system(f'libreoffice --headless --convert-to docx "{input_path}" --outdir "{UPLOAD_FOLDER}"')

        if not os.path.exists(output_path):
            return {"error": "Converted file not found"}, 500

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}, 500

if __name__ == "__main__":
    app.run(debug=True)
