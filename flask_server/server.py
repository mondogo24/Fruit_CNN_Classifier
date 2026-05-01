from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import base64
import os

app = Flask(__name__)

MODEL_PATH = './flask_server/fruit_classifier.keras' 
model = tf.keras.models.load_model(MODEL_PATH)

CLASSES = {0: 'Manzana', 1: 'Plátano', 2: 'Limón', 3: 'Naranja', 4: 'Pera'}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400
    
    encoded_data = data['image']
    decoded_bytes = base64.b64decode(encoded_data)
    img_array = np.frombuffer(decoded_bytes, dtype=np.float32).reshape((1, 64, 64, 3))
    
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction, axis=1)[0]
    
    return jsonify({
        'class': CLASSES[predicted_index],
        'confidence': float(np.max(prediction))
    })

if __name__ == '__main__':
    app.run(port=5000)