import os
from flask import Flask, request, send_file
import pdfplumber
import pandas as pd

app = Flask(__name__)

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
    output_filename = file.filename.rsplit(".", 1)[0] + ".xlsx"
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_filename)

    # Convert PDF to Excel
    try:
        with pdfplumber.open(input_path) as pdf:
            tables = []
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    tables.extend(table)

        if tables:
            df = pd.DataFrame(tables)
            df.to_excel(output_path, index=False)
        else:
            return {"error": "No tables detected in PDF"}, 400

    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}, 500

    # Ensure the file was created before sending it
    if not os.path.exists(output_path):
        return {"error": "Converted file not found"}, 500

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)


