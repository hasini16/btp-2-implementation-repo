import React, { useEffect, useState, useRef, useCallback } from 'react';
import toast from 'react-hot-toast';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { healthService, HealthResponse, ModelInfo } from '../services/api';

interface SensorRawData {
  time: string;
  accel_x_raw: number;
  accel_y_raw: number;
  accel_z_raw: number;
  accel_x_g: number;
  accel_y_g: number;
  accel_z_g: number;
  gyro_x: number;
  gyro_y: number;
  gyro_z: number;
  temperature?: number;
}

const LSB_PER_G = 2048;

const MachineHealth: React.FC = () => {
  const [rawBuffer, setRawBuffer] = useState<SensorRawData[]>([]);
  const [recentData, setRecentData] = useState<SensorRawData[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<string>('Disconnected');
  const [machineStatus, setMachineStatus] = useState<string>('Offline');
  const [prediction, setPrediction] = useState<HealthResponse | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const logRef = useRef<HTMLDivElement>(null);
  const [isPredictReady, setIsPredictReady] = useState(false);

  const addLog = useCallback((msg: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs((prev) => [...prev, `[${timestamp}] ${msg}`]);
  }, []);

  const scrollToBottom = () => {
    logRef.current?.scrollTo(0, logRef.current.scrollHeight);
  };

  useEffect(() => {
    scrollToBottom();
  }, [logs]);

  // Fetch model info
  useEffect(() => {
    healthService.getModelInfo()
      .then(setModelInfo)
      .catch((e) => addLog(`Model info fetch error: ${e.message}`));
  }, [addLog]);

  // Update predict ready
  useEffect(() => {
    setIsPredictReady(rawBuffer.length >= 4096);
  }, [rawBuffer.length]);

  // WS connection
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/api/live-feed/ws');

    ws.onopen = () => {
      setConnectionStatus('Connected');
      addLog('WebSocket connected to backend');
      toast.success('Live feed connected 📡');
    };

    ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data) as any;
        const newPoint: SensorRawData = {
          time: new Date().toLocaleTimeString(),
          accel_x_raw: parsed.accel_x || 0,
          accel_y_raw: parsed.accel_y || 0,
          accel_z_raw: parsed.accel_z || 0,
          accel_x_g: (parsed.accel_x || 0) / LSB_PER_G,
          accel_y_g: (parsed.accel_y || 0) / LSB_PER_G,
          accel_z_g: (parsed.accel_z || 0) / LSB_PER_G,
          gyro_x: parsed.gyro_x || 0,
          gyro_y: parsed.gyro_y || 0,
          gyro_z: parsed.gyro_z || 0,
          temperature: parsed.temperature,
        };

        setRawBuffer((prev) => {
          const updated = [...prev, newPoint];
          if (updated.length > 5000) { // Buffer safety
            updated.shift();
          }
          return updated;
        });

        setRecentData((prev) => {
          const updated = [...prev, newPoint];
          if (updated.length > 100) {
            updated.shift();
          }
          return updated;
        });

        // Machine status from recent RMS accel
        const recentRMS = recentData.slice(-10).reduce((sum, d) => sum + Math.sqrt(d.accel_x_g**2 + d.accel_y_g**2 + d.accel_z_g**2), 0) / 10;
        if (recentRMS > 2.0) {
          setMachineStatus('High Vibration ⚠️');
        } else if (recentRMS > 1.0) {
          setMachineStatus('Normal');
        } else {
          setMachineStatus('Optimal');
        }

        addLog(`New sample #${rawBuffer.length + 1}, RMS: ${recentRMS.toFixed(2)}g`);

      } catch (e) {
        addLog(`Parse error: ${(e as Error).message}`);
      }
    };

    ws.onclose = () => {
      setConnectionStatus('Disconnected');
      setMachineStatus('Offline');
      toast.error('Live feed disconnected ❌');
      addLog('WebSocket disconnected');
    };

    ws.onerror = (e) => {
      setConnectionStatus('Error');
      addLog('WebSocket error');
    };

    return () => ws.close();
  }, [addLog, rawBuffer.length, recentData]);

  const handlePredict = async () => {
    if (!isPredictReady) {
      toast.error('Need at least 4096 samples for prediction');
      return;
    }

    const rawSeq = rawBuffer.slice(-4096).map((d) => [d.accel_x_raw, d.accel_y_raw, d.accel_z_raw]);
    try {
      const pred = await healthService.predictHealth(rawSeq);
      setPrediction(pred);
      const statusColor = pred.health_status === 'Good' ? 'success' : 'error';
      toast[`${statusColor}`](`Health: ${pred.health_status} (Bad prob: ${pred.bad_probability.toFixed(3)})`);
      addLog(`CNN Prediction: ${pred.health_status} (conf: ${pred.confidence.toFixed(2)})`);
    } catch (e) {
      toast.error('Prediction failed');
      addLog(`Predict error: ${(e as Error).message}`);
    }
  };

  const recentRaw = rawBuffer.slice(-20);

  const getStatusClass = (status: string) => {
    if (status === 'Connected') return 'text-healthy';
    if (status.includes('High Vibration')) return 'text-warning';
    if (status === 'Error') return 'text-critical';
    return '';
  };

  return (
    <div className="module-container">
      <h2>Live Machine Health Dashboard</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '24px' }}>
        ESP32S2 Indusboard V2 telemetry → real-time charts → CNN Good/Bad prediction
      </p>

      {/* Status Cards */}
      <div className="status-indicators">
        <div className="status-card">
          <div className="status-label">Connection</div>
          <div className={`status-value ${getStatusClass(connectionStatus)}`}>
            {connectionStatus}
          </div>
        </div>
        <div className="status-card">
          <div className="status-label">Machine Status</div>
          <div className={`status-value ${getStatusClass(machineStatus)}`}>
            {machineStatus}
          </div>
        </div>
        <div className="status-card">
          <div className="status-label">Buffer Samples</div>
          <div className="status-value">{rawBuffer.length.toLocaleString()}</div>
        </div>
        <div className="status-card">
          <div className="status-label">Predict Ready</div>
          <div className={`status-value ${isPredictReady ? 'text-healthy' : 'text-neutral'}`}>
            {isPredictReady ? 'YES' : 'NO'}
          </div>
        </div>
      </div>

      {/* Prediction Button */}
      <div style={{ marginBottom: '24px' }}>
        <button className="action-btn" onClick={handlePredict} disabled={!isPredictReady}>
          {isPredictReady ? 'Run CNN Health Prediction' : 'Collecting 4096 samples...'}
        </button>
      </div>

      {/* Prediction Result */}
      {prediction && (
        <div className="status-card" style={{ marginBottom: '24px', backgroundColor: prediction.health_status === 'Good' ? '#d4f4e2' : '#f8d7da' }}>
          <div className="status-label">Latest CNN Prediction</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
            {prediction.health_status}
          </div>
          <div>Bad Prob: {prediction.bad_probability.toFixed(3)} (Conf: {prediction.confidence.toFixed(3)})</div>
        </div>
      )}

      {/* Model Info */}
      {modelInfo && (
        <div className="status-card" style={{ marginBottom: '24px' }}>
          <div className="status-label">Model Info</div>
          <div>{modelInfo.description}</div>
          <div style={{ fontSize: '14px', color: 'var(--text-muted)' }}>
            Input: {modelInfo.input_shape} | Output: {modelInfo.output_shape}
          </div>
        </div>
      )}

      {/* Live Charts */}
      <div className="chart-container">
        <h3>Live Acceleration (g) - Recent 100 Samples</h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={recentData}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="time" />
            <YAxis domain={['dataMin - 0.5', 'dataMax + 0.5']} tickFormatter={(v) => `${v.toFixed(2)}g`} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="accel_x_g" stroke="#3b82f6" name="Accel X" />
            <Line type="monotone" dataKey="accel_y_g" stroke="#10b981" name="Accel Y" />
            <Line type="monotone" dataKey="accel_z_g" stroke="#f59e0b" name="Accel Z" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Raw Data Table */}
      <div className="chart-container">
        <h3>Raw Sensor Data (Last 20 Samples)</h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: 'var(--bg-tertiary)' }}>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid var(--border-color)' }}>Time</th>
                <th style={{ padding: '12px', textAlign: 'right' }}>Ax Raw (g)</th>
                <th style={{ padding: '12px', textAlign: 'right' }}>Ay Raw (g)</th>
                <th style={{ padding: '12px', textAlign: 'right' }}>Az Raw (g)</th>
              </tr>
            </thead>
            <tbody>
              {recentRaw.map((d, i) => (
                <tr key={i}>
                  <td style={{ padding: '12px', fontFamily: 'monospace' }}>{d.time}</td>
                  <td style={{ padding: '12px', textAlign: 'right', fontFamily: 'monospace' }}>{d.accel_x_raw} ({d.accel_x_g.toFixed(3)})</td>
                  <td style={{ padding: '12px', textAlign: 'right', fontFamily: 'monospace' }}>{d.accel_y_raw} ({d.accel_y_g.toFixed(3)})</td>
                  <td style={{ padding: '12px', textAlign: 'right', fontFamily: 'monospace' }}>{d.accel_z_raw} ({d.accel_z_g.toFixed(3)})</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Logs Panel */}
      <div className="chart-container">
        <h3>Event Logs (Last 20)</h3>
        <div ref={logRef} className="logs-panel" style={{ height: '200px', overflowY: 'auto', background: 'var(--bg-tertiary)', padding: '16px', borderRadius: '8px', fontFamily: 'monospace', fontSize: '14px', border: '1px solid var(--border-color)' }}>
          {logs.slice(-20).map((log, i) => <div key={i}>{log}</div>)}
        </div>
      </div>
    </div>
  );
};

export default MachineHealth;
