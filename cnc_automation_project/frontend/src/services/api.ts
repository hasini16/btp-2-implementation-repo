import axios from 'axios';

// Ensure this matches the port your FastAPI server is running on
const API_BASE_URL = 'http://localhost:8000/api';

// ==========================================
// INTERFACES (Type Definitions)
// ==========================================

// --- RUL Prediction Interfaces ---
export interface PredictionResponse {
    status: string;
    remaining_useful_life_hours: number;
    model_status: string;
}

// --- CAD Processing Interfaces ---
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


// ==========================================
// API SERVICES
// ==========================================

export const rulService = {
    /**
     * Sends a 2D array of sensor data to the CNN-LSTM model for RUL prediction.
     */
    predictRUL: async (sensorData: number[][]): Promise<PredictionResponse> => {
        try {
            const response = await axios.post<PredictionResponse>(`${API_BASE_URL}/predict-rul`, {
                sequence_data: sensorData
            });
            return response.data;
        } catch (error) {
            console.error("Error fetching RUL prediction:", error);
            throw error;
        }
    }
};

export const cadService = {
    /**
     * Triggers the SolidWorks COM interface to open a part, run AFR, and generate G-code.
     */
    processCADFile: async (filePath: string): Promise<CADResponse> => {
        try {
            const response = await axios.post<CADResponse>(`${API_BASE_URL}/process-cad`, {
                file_path: filePath
            });
            return response.data;
        } catch (error) {
            console.error("Error processing CAD file:", error);
            throw error;
        }
    }
};