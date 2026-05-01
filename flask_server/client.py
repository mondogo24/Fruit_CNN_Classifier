import gradio as gr
import requests
import numpy as np
from PIL import Image
import base64
import io

SERVER_URL = "http://localhost:5000/predict"

def preprocess_and_send(image):
    image = image.convert('RGB')
    image = image.resize((64, 64))
    img_array = np.array(image, dtype=np.float32)
    img_array = (img_array / 127.5) - 1

    img_bytes = img_array.tobytes()
    encoded_img = base64.b64encode(img_bytes).decode('utf-8')
    response = requests.post(SERVER_URL, json={'image': encoded_img})
    
    if response.status_code == 200:
        result = response.json()
        return f"Predicción: {result['class']} ({result['confidence']:.2%})"
    else:
        return "Error en la conexión con el servidor"

demo = gr.Interface(
    fn=preprocess_and_send,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="Clasificador de Frutas"
)

if __name__ == "__main__":
    demo.launch()