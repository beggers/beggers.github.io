import React from 'react';
import ReactDOM from 'react-dom/client';
import { Canvas } from '@react-three/fiber'
import App from './App';

const root = ReactDOM.createRoot(document.querySelector('#root'));
root.render(
    <Canvas camera={{
        fov: 75,
        near: 0.1,
        far: 100,
        position: [0, 0, 30],
    }} >
        <App />
    </Canvas>
);