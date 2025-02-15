import os
from flask import Flask, request, send_file

app = Flask(__name__)

UPLOAD_FOLDER = "/tmp/"  # Save files in Render's temp directory
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

    # Save file to /tmp/ directory
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(input_path)

    # Generate output file name
    output_filename = file.filename.rsplit(".", 1)[0] + ".xlsx"
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_filename)

    # Run conversion (Replace this with actual PDF to Excel conversion logic)
    # Example: Convert PDF to Excel (Dummy placeholder)
    os.system(f"cp {input_path} {output_path}")  # Replace with actual conversion logic

    # Ensure the converted file exists
    if not os.path.exists(output_path):
        return {"error": "Conversion failed"}, 500

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

