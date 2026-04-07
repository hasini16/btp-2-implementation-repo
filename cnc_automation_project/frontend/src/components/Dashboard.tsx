import React, { useState } from 'react';
import { rulService, cadService, } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Dashboard.css';

// Interface for the Recharts graph data
interface ChartDataPoint {
    time: number;
    Vibration: number;
    Temperature: number;
}
export interface PredictionResponse {
    status: string;
    remaining_useful_life_hours: number;
    model_status: string;
} 

export interface ExtractedFeatures {
    faces: number;
    edges: number;
    vertices: number;
    recognized_features: string[];
} 

export interface CADResponse {
    status: string;
    extracted_features: ExtractedFeatures;
    gcode_generation: string;
}


const Dashboard: React.FC = () => {
    // --- State: CAD/CAM Automation ---
    const [filePath, setFilePath] = useState<string>('C:\\Models\\test_part.SLDPRT');
    const [cadResult, setCadResult] = useState<CADResponse | null>(null);
    const [cadLoading, setCadLoading] = useState<boolean>(false);

    // --- State: Predictive Maintenance (RUL) ---
    const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
    const [rulLoading, setRulLoading] = useState<boolean>(false);
    const [chartData, setChartData] = useState<ChartDataPoint[]>([]);

    // --- Handlers ---
    const runCADProcess = async () => {
        setCadLoading(true);
        try {
            const result = await cadService.processCADFile(filePath);
            setCadResult(result);
        } catch (error) {
            console.error("CAD Processing failed:", error);
            alert("Failed to process CAD file. Is SolidWorks running?");
        } finally {
            setCadLoading(false);
        }
    };

    const runPrediction = async () => {
        setRulLoading(true);
        
        // Generate 50 timesteps of fake sensor data
        const fakeSequence: number[][] = Array.from({ length: 50 }, () => [
            Math.random(), Math.random(), Math.random(), Math.random()
        ]);
        
        // Format for the Recharts component
        const formattedChartData: ChartDataPoint[] = fakeSequence.map((step, index) => ({
            time: index,
            Vibration: step[0],
            Temperature: step[1],
        }));

        try {
            const result = await rulService.predictRUL(fakeSequence);
            setPrediction(result);
            setChartData(formattedChartData);
        } catch (error) {
            console.error("Prediction failed:", error);
        } finally {
            setRulLoading(false); 
        }
    };

    // Helper for styling status text
    const getStatusClass = (status: string) => {
        if (status === 'Healthy') return 'status-healthy';
        if (status.includes('Warning')) return 'status-warning';
        return 'status-critical';
    };

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <h2 className="dashboard-title">CNC Automation & Health Monitor</h2>
            </div>

            {/* ========================================== */}
            {/* MODULE 1: CAD/CAM AUTOMATION               */}
            {/* ========================================== */}
            <div className="chart-container" style={{ marginBottom: '2rem' }}>
                <h3 className="chart-title" style={{ marginBottom: '1rem' }}>1. CAD/CAM Automation (SolidWorks)</h3>
                
                <div style={{ display: 'flex', gap: '10px', marginBottom: '1.5rem' }}>
                    <input 
                        type="text" 
                        value={filePath}
                        onChange={(e) => setFilePath(e.target.value)}
                        placeholder="Enter absolute path to .SLDPRT file..."
                        style={{ flex: 1, padding: '0.75rem', borderRadius: '6px', border: '1px solid #e1e8ed', fontSize: '1rem' }}
                    />
                    <button 
                        className="action-btn"
                        onClick={runCADProcess} 
                        disabled={cadLoading || !filePath}
                    >
                        {cadLoading ? 'Connecting to COM...' : 'Run AFR & Generate G-Code'}
                    </button>
                </div>

                {cadResult && (
                    <div className="status-card" style={{ marginBottom: '0', backgroundColor: '#f9fbfd' }}>
                        <div className="status-card-grid">
                            <div className="status-item">
                                <span className="status-label">Process Status</span>
                                <span className="status-value status-healthy">{cadResult.status}</span>
                            </div>
                            <div className="status-item">
                                <span className="status-label">B-Rep Faces Detected</span>
                                <span className="status-value">{cadResult.extracted_features.faces}</span>
                            </div>
                            <div className="status-item">
                                <span className="status-label">B-Rep Edges Detected</span>
                                <span className="status-value">{cadResult.extracted_features.edges}</span>
                            </div>
                            <div className="status-item">
                                <span className="status-label">CAMWorks Post-Processing</span>
                                <span className="status-value status-healthy">{cadResult.gcode_generation}</span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* ========================================== */}
            {/* MODULE 2: PREDICTIVE MAINTENANCE           */}
            {/* ========================================== */}
            <div className="chart-container" style={{ marginBottom: '2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                    <h3 className="chart-title" style={{ margin: 0 }}>2. Predictive Maintenance (CNN-LSTM)</h3>
                    <button 
                        className="action-btn"
                        onClick={runPrediction} 
                        disabled={rulLoading}
                    >
                        {rulLoading ? 'Running Neural Network...' : 'Simulate Sensor Data & Predict RUL'}
                    </button>
                </div>

                {prediction && (
                    <div className="status-card" style={{ marginBottom: '1.5rem', backgroundColor: '#f9fbfd' }}>
                        <div className="status-card-grid">
                            <div className="status-item">
                                <span className="status-label">Machine Health Status</span>
                                <span className={`status-value ${getStatusClass(prediction.status)}`}>
                                    {prediction.status}
                                </span>
                            </div>
                            <div className="status-item">
                                <span className="status-label">Remaining Useful Life (RUL)</span>
                                <span className="status-value">{prediction.remaining_useful_life_hours} Hours</span>
                            </div>
                            <div className="status-item">
                                <span className="status-label">Model Status</span>
                                <span className="status-value">{prediction.model_status}</span>
                            </div>
                        </div>
                    </div>
                )}

                {chartData.length > 0 && (
                    <div>
                        <h4 className="chart-title" style={{ fontSize: '1rem', color: '#7f8c8d' }}>Live Sensor Feed (Vibration & Temp)</h4>
                        <div className="chart-wrapper">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={chartData}>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                    <XAxis dataKey="time" tick={{fill: '#7f8c8d'}} />
                                    <YAxis tick={{fill: '#7f8c8d'}} />
                                    <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }} />
                                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                                    <Line type="monotone" dataKey="Vibration" stroke="#8884d8" strokeWidth={2} dot={false} activeDot={{ r: 8 }} />
                                    <Line type="monotone" dataKey="Temperature" stroke="#82ca9d" strokeWidth={2} dot={false} activeDot={{ r: 8 }} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;