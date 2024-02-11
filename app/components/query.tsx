import { useState } from "react";
import Image from "next/image";
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

export default function TextBox() {
    const [value, setValue] = useState("");
    const [image, setImage] = useState("");

    async function handleSubmit() {
        socket.emit('image query', {value});
        setValue('');
    };

    socket.on('image query', (image_info) => {
      let images = [image_info.imageData];
      setImage(images[0]);
    });

  return (
    <div>
      <div className="flex-row">
          <input
          type="textarea"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="p-2 border-2 border-gray-300 w-80"
          />
          <button onClick={handleSubmit} className="bg-gray-300 border-2 border-gray-400 p-2"> Submit </button>
      </div>
      <div>
          <Image id="generatedImage" src={image} alt="image"/>
      </div>
    </div>
  );
}
