import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface HealthResponse {
  health_status: string;
  bad_probability: number;
  confidence: number;
  threshold: number;
}

export interface ModelInfo {
  input_shape: string;
  output_shape: string;
  summary_top: string;
  description: string;
}

export const healthService = {
  predictHealth: async (rawSequence: number[][]): Promise<HealthResponse> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/ml/predict-health`, {
        raw_sequence: rawSequence
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching health prediction:", error);
      throw error;
    }
  },
  getModelInfo: async (): Promise<ModelInfo> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/ml/model-info`);
      return response.data;
    } catch (error) {
      console.error("Error fetching model info:", error);
      throw error;
    }
  }
};
