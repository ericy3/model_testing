from flask import Flask
from flask_socketio import SocketIO, emit
import torch
from diffusers import DiffusionPipeline
from PIL import Image

app = Flask(__name__)
socketio = SocketIO(app)

# Load the Stable Diffusion model
device = "cuda" if torch.cuda.is_available() else "cpu"
pipeline = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4").to(device)

# Handle WebSocket connections
@socketio.on('image query')
def handle_image_query(text):
    try:
        # Generate images based on the input text
        with torch.no_grad():
            generated_images = pipeline.generate(text, device=device)

        # Convert generated images to PIL Image objects
        images = [Image.fromarray(img.permute(1, 2, 0).cpu().numpy()) for img in generated_images]

        # Send the generated images back to the client
        for image in images:
            emit('image query', image.tobytes(), binary=True)
    except Exception as e:
        print('Error generating images:', e)

# Handle disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print('User disconnected')

if __name__ == '__main__':
    socketio.run(app, port=5000)
