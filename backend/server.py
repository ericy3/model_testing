from flask import Flask
from flask_socketio import SocketIO, emit
import torch
from diffusers import DiffusionPipeline
from PIL import Image


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load the Stable Diffusion model
device = "cuda" if torch.cuda.is_available() else "cpu"
pipeline = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4").to(device)

# Handle WebSocket connections
@socketio.on('image query')
def handle_image_query(data):
    try:
        # Ensure the input is text
        text = data.get('text')
        if not text:
            emit('error', {'error': 'No text provided'})
            return
        # Generate an image based on the input text
        with torch.no_grad():
            generated_images = pipe([text], num_inference_steps=50)  # Adjust num_inference_steps as needed
        # Convert the generated image to a PIL Image object
        image = generated_images.images[0]
        # Convert PIL Image to bytes (example: PNG format)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        # Send the generated image back to the client
        emit('image response', img_byte_arr, binary=True)
    except Exception as e:
        emit('error', {'error': str(e)})
        print('Error generating images:', e)
# Handle disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print('User disconnected')
if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)
