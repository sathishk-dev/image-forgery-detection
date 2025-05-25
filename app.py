from flask import Flask, render_template, request
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from io import BytesIO
import base64

app = Flask(__name__)

model = load_model('./models/image_forgery_detection_casia2.h5')

image_size = (128, 128)

def rbg_lab_preprocess(image, quality):
    temp_io = BytesIO()
    image.save(temp_io, format='JPEG', quality=quality)
    temp_io.seek(0)
    temp_image = Image.open(temp_io)

    ela_image = ImageChops.difference(image, temp_image)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    max_diff = max_diff if max_diff != 0 else 1
    scale = 255.0 / max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    ela_cv = np.array(ela_image)
    ela_cv = cv2.cvtColor(ela_cv, cv2.COLOR_RGB2BGR)

    gray_rgb = cv2.cvtColor(ela_cv, cv2.COLOR_BGR2GRAY)
    edges_rgb = cv2.Canny(gray_rgb, 50, 150)

    lab_image = cv2.cvtColor(ela_cv, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)
    edges_lab = cv2.bitwise_or(cv2.Canny(l, 50, 150), cv2.Canny(a, 50, 150))
    edges_lab = cv2.bitwise_or(edges_lab, cv2.Canny(b, 50, 150))

    combined_edges = cv2.bitwise_or(edges_rgb, edges_lab)
    edges_colored = cv2.cvtColor(combined_edges, cv2.COLOR_GRAY2BGR)
    final_result = cv2.addWeighted(ela_cv, 0.9, edges_colored, 0.1, 0)
    final_result = cv2.cvtColor(final_result, cv2.COLOR_BGR2RGB)

    return Image.fromarray(final_result)

def prepare_image(image):
    return np.array(rbg_lab_preprocess(image, 90).resize(image_size)).flatten() / 255.0

def prepare_image_for_prediction(image):
    img_array = prepare_image(image)
    return img_array.reshape(1, 128, 128, 3)

def image_to_base64(img):
    buf = BytesIO()
    img.save(buf, format='PNG')
    base64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{base64_str}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'

    image = Image.open(file.stream).convert('RGB')

    # Predict
    prepared_image = prepare_image_for_prediction(image)
    prediction = model.predict(prepared_image)
    predicted_class = np.argmax(prediction)
    confidence_score = prediction[0][predicted_class] * 100
    labels = ['Fake', 'Real']
    prediction_label = labels[predicted_class]

    processed_image = rbg_lab_preprocess(image, 90).resize((256, 256))
    original_image = image.resize((256, 256))

    # Encode images to base64
    original_b64 = image_to_base64(original_image)
    processed_b64 = image_to_base64(processed_image)

    return render_template('result.html',
                           original=original_b64,
                           ela=processed_b64,
                           prediction=prediction_label,
                           confidence=f"{confidence_score:.2f}")

if __name__ == '__main__':
    app.run(debug=True)
