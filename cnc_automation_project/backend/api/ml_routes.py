from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import os

# Import ML modules
from ml_models.cnn_lstm import RULPredictor

router = APIRouter()

# --- Initialize the ML Model ---
model_file_path = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'saved_models', 'cnn_lstm_rul.keras')
predictor = RULPredictor(model_path=model_file_path)

class SensorData(BaseModel):
    # Expecting time-series data: a list of timesteps, where each timestep is a list of sensor features
    sequence_data: list[list[float]]

@router.post("/predict-rul")
async def predict_remaining_useful_life(data: SensorData):
    """
    Endpoint to receive time-series sensor data, reshape it, 
    and return the RUL prediction from the CNN-LSTM model.
    """
    if predictor.model is None:
        return {
            "status": "Model not trained yet. Returning dummy data.",
            "remaining_useful_life_hours": 124.5,
            "model_status": "Inactive"
        }
        
    try:
        input_array = np.array([data.sequence_data])
        
        rul_prediction = predictor.predict(input_array)
        
        if rul_prediction < 50:
            health_status = "Critical - Maintenance Required"
        elif rul_prediction < 150:
            health_status = "Warning - Monitor Closely"
        else:
            health_status = "Healthy"
            
        return {
            "status": health_status,
            "remaining_useful_life_hours": round(rul_prediction, 2),
            "model_status": "Active"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
