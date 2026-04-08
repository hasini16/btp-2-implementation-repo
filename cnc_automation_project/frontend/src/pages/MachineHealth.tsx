import React, { useEffect, useState, useRef } from 'react';
import toast from 'react-hot-toast';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface SensorData {
  time: string;
  accel_x: number;
  accel_y: number;
  accel_z: number;
  gyro_x: number;
  gyro_y: number;
  gyro_z: number;
  temperature: number;
}

const MachineHealth: React.FC = () => {
  const [data, setData] = useState<SensorData[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<string>('Connecting...');
  const [machineStatus, setMachineStatus] = useState<string>('Awaiting Data...');

  // Ref to throttle toast warnings
  const lastWarningTime = useRef<number>(0);

  useEffect(() => {
    // Connect to the FastAPI WebSocket
    const ws = new WebSocket('ws://localhost:8000/api/live-feed/ws');

    ws.onopen = () => {
      setConnectionStatus('Socket Connected');
      toast.success('Live telemetry stream connected.', { icon: '📡' });
      setMachineStatus('Monitoring...');
    };

    ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        const newDataPoint: SensorData = {
          time: new Date().toLocaleTimeString(),
          accel_x: parsed.accel_x || 0,
          accel_y: parsed.accel_y || 0,
          accel_z: parsed.accel_z || 0,
          gyro_x: parsed.gyro_x || 0,
          gyro_y: parsed.gyro_y || 0,
          gyro_z: parsed.gyro_z || 0,
          temperature: parsed.temperature || 0,
        };

        setData((prevData) => {
          const updatedData = [...prevData, newDataPoint];
          if (updatedData.length > 20) {
            updatedData.shift();
          }
          return updatedData;
        });

        // Machine status logic
        if (Math.abs(newDataPoint.accel_x) > 2.0 || Math.abs(newDataPoint.accel_y) > 2.0) {
          setMachineStatus('Warning: High Vibration');

          // Throttle warning toast to max once every 10 seconds
          const now = Date.now();
          if (now - lastWarningTime.current > 10000) {
            toast.error('High vibration anomalous spike detected!', { id: 'vibration-spike' });
            lastWarningTime.current = now;
          }
        } else {
          setMachineStatus('Optimal');
        }

      } catch (e) {
        console.error("Error parsing websocket data", e);
      }
    };

    ws.onclose = () => {
      setConnectionStatus('Disconnected');
      setMachineStatus('Offline');
      toast.error('Telemetry stream disconnected.', { icon: '❌' });
    };

    ws.onerror = () => {
      setConnectionStatus('WebSocket Error');
      setMachineStatus('Error');
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="module-container">
      <h2>Machine Health & Predictive Maintenance</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '24px' }}>
        Real-time telemetry from MPU6050 vibration analysis hooked into the CNN-LSTM predictor model.
      </p>

      <div className="status-indicators">
        <div className="status-card">
          <div className="status-label">Network Link</div>
          <div className={`status-value ${connectionStatus === 'Socket Connected' ? 'text-healthy' : 'text-critical'}`}>
            {connectionStatus}
          </div>
        </div>
        <div className="status-card">
          <div className="status-label">Mechanical Status</div>
          <div className={`status-value ${machineStatus === 'Optimal' ? 'text-healthy' : machineStatus.includes('Warning') ? 'text-warning' : 'text-neutral'}`}>
            {machineStatus}
          </div>
        </div>
        <div className="status-card">
          <div className="status-label">Live Packets Sampled</div>
          <div className="status-value">{data.length > 0 ? 'Active Stream' : 'Awaiting sync...'}</div>
        </div>
      </div>

      <div className="chart-container" style={{ width: '100%', height: 450, marginTop: '16px' }}>
        <h3 style={{ marginBottom: '16px' }}>Live Vibration Feed (MPU6050 Accel)</h3>
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="time" />
            <YAxis
              domain={[-0.5, 2.5]} // Allow for slight negative readings if the sensor shifts
              tickCount={7}
              tickFormatter={(value) => `${value.toFixed(1)} g`} // Adds the unit
              width={60} // Ensures enough space for the labels
            />
            <Tooltip contentClassName="tooltip-custom" />
            <Legend wrapperStyle={{ paddingTop: '10px' }} />
            <Line type="monotone" dataKey="accel_x" stroke="var(--accent-blue)" strokeWidth={2} animationDuration={300} dot={false} />
            <Line type="monotone" dataKey="accel_y" stroke="var(--status-healthy)" strokeWidth={2} animationDuration={300} dot={false} />
            <Line type="monotone" dataKey="accel_z" stroke="var(--status-warning)" strokeWidth={2} animationDuration={300} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default MachineHealth;
