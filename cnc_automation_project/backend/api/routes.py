from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import os

# Import CAD modules
from cad_integration.sw_connection import SolidWorksConnection
from cad_integration.feature_recognition import FeatureRecognizer
from cad_integration.gcode_generator import CAMWorksIntegrator

# Import ML modules
from ml_models.cnn_lstm import RULPredictor

router = APIRouter()

# --- Initialize the ML Model ---
# We initialize it once when the server starts so it doesn't reload on every request.
# Make sure the path points correctly relative to where you run app.py
model_file_path = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'saved_models', 'cnn_lstm_rul.keras')
predictor = RULPredictor(model_path=model_file_path)

# --- Pydantic Models for Request Validation ---
class CADRequest(BaseModel):
    file_path: str

class SensorData(BaseModel):
    # Expecting time-series data: a list of timesteps, where each timestep is a list of sensor features
    # Example shape: 50 timesteps, each with 4 sensor readings
    sequence_data: list[list[float]]

# --- API Endpoints ---

@router.post("/process-cad")
async def process_cad_file(request: CADRequest):
    """
    Endpoint to open a SolidWorks part, extract B-rep data, 
    and generate G-code via CAMWorks.
    """
    if not os.path.exists(request.file_path):
        raise HTTPException(status_code=404, detail="CAD file not found on server.")

    sw_conn = SolidWorksConnection()
    
    if not sw_conn.connect():
        raise HTTPException(status_code=500, detail="Failed to connect to SolidWorks COM interface.")

    try:
        model = sw_conn.open_part(request.file_path)
        if not model:
            raise HTTPException(status_code=500, detail="Failed to open the part file.")

        recognizer = FeatureRecognizer(model)
        brep_data = recognizer.extract_brep_data()

        cam_integrator = CAMWorksIntegrator(sw_conn.sw_app)
        if cam_integrator.load_camworks_addin():
            output_gcode_path = request.file_path.replace('.SLDPRT', '.nc')
            cam_integrator.run_kbm_and_generate_gcode(output_gcode_path)
            gcode_status = "Success"
        else:
            gcode_status = "Failed to load CAMWorks"

        return {
            "status": "Processing Complete",
            "extracted_features": brep_data,
            "gcode_generation": gcode_status
        }

    finally:
        sw_conn.disconnect()

@router.post("/predict-rul")
async def predict_remaining_useful_life(data: SensorData):
    """
    Endpoint to receive time-series sensor data, reshape it, 
    and return the RUL prediction from the CNN-LSTM model.
    """
    # 1. Check if the model is actually loaded and ready
    if predictor.model is None:
        return {
            "status": "Model not trained yet. Returning dummy data.",
            "remaining_useful_life_hours": 124.5,
            "model_status": "Inactive"
        }
        
    # 2. If the model exists, process the real prediction
    try:
        # Convert incoming JSON list to a 3D numpy array: (1 sample, timesteps, features)
        input_array = np.array([data.sequence_data])
        
        # Get prediction
        rul_prediction = predictor.predict(input_array)
        
        # Determine machine health status based on thresholds
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