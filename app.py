import os
from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfMerger, PdfReader

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Free PDF Utility Hub</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; background: #f4f4f9; text-align: center; }
            .box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
            input[type="file"], input[type="submit"] { margin-top: 15px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; width: 100%; box-sizing: border-box; }
            input[type="submit"] { background: #007BFF; color: white; border: none; cursor: pointer; font-size: 16px; }
            input[type="submit"]:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>⚡ Free PDF Utility Hub</h1>
        <div class="box">
            <h3>1. Merge Multiple PDFs</h3>
            <form action="/merge" method="post" enctype="multipart/form-data">
                <input type="file" name="files" multiple required>
                <input type="submit" value="Merge PDFs">
            </form>
        </div>
        <div class="box">
            <h3>2. Extract Text from PDF</h3>
            <form action="/extract" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <input type="submit" value="Extract Text">
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    uploaded_files = request.files.getlist('files')
    merger = PdfMerger()
    output_path = os.path.join(UPLOAD_FOLDER, "merged.pdf")
    for file in uploaded_files:
        merger.append(file)
    merger.write(output_path)
    merger.close()
    return send_file(output_path, as_attachment=True)

@app.route('/extract', methods=['POST'])
def extract_text():
    file = request.files['file']
    reader = PdfReader(file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text() + "\n"
    return f"<h3>Extracted Text:</h3><pre style='text-align:left; background:#fff; padding:15px; border:1px solid #ccc;'>{extracted_text}</pre><br><a href='/'>Go Back</a>"

if __name__ == '__main__':
    app.run(debug=True)
