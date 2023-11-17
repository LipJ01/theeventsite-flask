from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from flask_cors import CORS
from io import BytesIO
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB, adjust as needed
IMAGE_DIR = 'images'
CORS(app)


@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    if file:
        try:
            # save image to disk
            filename = file.filename if file.filename else 'unknown.png'
            path = os.path.join(IMAGE_DIR, filename)
            file.save(path)
            return jsonify({'image': file.read().decode('utf-8')}), 200
        except Exception as e:
            return jsonify({'error': 'Error converting image to text: {}'.format(str(e))}), 500
    else:
        return jsonify({'error': 'Invalid file'}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
