from flask import Flask, request, jsonify
from PIL import Image
from werkzeug.utils import secure_filename
import os
import tempfile
from preprocessBatch import preprocessing
from keras.models import load_model
import cv2
import numpy as np
import uuid  # Use uuid to generate unique file names

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    allowedChars = '234579ACFHKMNPQRTYZ'
    WIDTH = 140
    HEIGHT = 48

    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify(success=False, captcha="No image file part")

    file = request.files['file']

    # Create a unique filename using uuid
    filename = secure_filename(str(uuid.uuid4()))

    # Save file to temp path
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, filename)
    file.save(temp_path)

    img = Image.open(temp_path)
    img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)
    # convert rgba to rgb
    img = img.convert('RGB')

    # Save processed image to temp path
    temp_path_processed = os.path.join(temp_dir, 'captcha.jpg')
    img.save(temp_path_processed, "JPEG")

    preprocessing(temp_path_processed, temp_path_processed)

    train_data = np.stack([np.array(cv2.imread(temp_path_processed))/255.0])
    model = load_model("thsrc_cnn_model.hdf5")
    prediction = model.predict(train_data)

    predict_captcha = ''
    for predict in prediction:
        value = np.argmax(predict[0])
        predict_captcha += allowedChars[value]

    # Remove temp files
    os.remove(temp_path)
    os.remove(temp_path_processed)

    return jsonify(success=True, captcha=predict_captcha)

if __name__ == "__main__":
    app.run(debug=True)
