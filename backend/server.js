const express = require('express');
const bodyParser = require('body-parser');
const http = require('http');
const { Server } = require('socket.io');
const { TextGenerationPipeline } = require('@transformers/text-generation');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(bodyParser.json());

// Load the Hugging Face model for text generation
const model = new TextGenerationPipeline({ model: 'gpt2' });

// Handle WebSocket connections
io.on('connection', (socket) => {
  console.log('A user connected');

  // Listen for messages from the client
  socket.on('image query', async (message) => {
    try {
      // Generate text based on the input message
      const generatedText = model(message, { max_length: 50 });

      // Send the generated response back to the client
      io.emit('image query', generatedText[0].generated_text);
    } catch (error) {
      console.error('Error generating text:', error);
    }
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    console.log('User disconnected');
  });
});

server.listen(5000, () => {
  console.log('Server is running on port 5000');
});