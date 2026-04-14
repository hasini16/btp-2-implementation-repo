import React from 'react';
import { Toaster } from 'react-hot-toast';
import MachineHealth from './pages/MachineHealth';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="app-container">
      <Toaster 
        position="top-right"
        toastOptions={{
          className: '',
          style: {
            background: '#192235',
            color: '#f8fafc',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)',
          },
        }}
      />
      <div className="header">
        <h1>ESP32S2 Machine Health Monitor</h1>
        <p>Real-time remote monitoring with CNN predictions</p>
      </div>
      <MachineHealth />
    </div>
  );
};

export default App;
