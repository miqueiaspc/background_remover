from flask import Flask, render_template, request, send_file, redirect, url_for
from rembg import remove
from PIL import Image
import os
from io import BytesIO
import zipfile 

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('images')
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file in files:
            image = Image.open(file.stream)
            output = remove(image)
            output_io = BytesIO()
            output.save(output_io, format='PNG')
            output_io.seek(0)
            zip_file.writestr(file.filename.replace('.jpg', '.png'), output_io.read())

    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name='imagens_sem_fundo.zip', mimetype='application/zip')

if __name__ == '__main__':
    app.run(debug=True)