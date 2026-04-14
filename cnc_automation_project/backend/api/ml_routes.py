from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import os
import tensorflow as tf
import logging

logger = logging.getLogger(__name__)

WINDOW_SIZE = 4096
LSB_PER_G = 2048

# Load CNN model for binary Good/Bad classification
model_path = os.path.join(os.path.dirname(__file__), '..', 'saved_models', 'final_cnn_model.keras')
model = tf.keras.models.load_model(model_path)
logger.info(f"Loaded model from {model_path}")

router = APIRouter()



class HealthData(BaseModel):
    raw_sequence: list[list[int]]  # 4096 x [accel_x_raw, accel_y_raw, accel_z_raw]

@router.post("/predict-health")
async def predict_machine_health(data: HealthData):
    """
    Binary classification Good/Bad using CNN on 4096x3 accel data (raw -> g).
    """
    logger.info("Health prediction requested")
    try:
        seq = np.array(data.raw_sequence, dtype=float) / LSB_PER_G
        if seq.shape != (WINDOW_SIZE, 3):
            raise HTTPException(status_code=400, detail=f"Expected shape ({WINDOW_SIZE},3), got {seq.shape}")
        input_array = seq.reshape(1, WINDOW_SIZE, 3)
        prob_bad = model.predict(input_array, verbose=0)[0][0]
        status = "Bad" if prob_bad > 0.5 else "Good"
        confidence = max(prob_bad, 1 - prob_bad)
        logger.info(f"Prediction: {status} (bad_prob: {prob_bad:.3f})")
        return {
            "health_status": status,
            "bad_probability": float(prob_bad),
            "confidence": float(confidence),
            "threshold": 0.5
        }
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/model-info")
async def get_model_info():
    """
    Model metadata and summary.
    """
    logger.info("Model info requested")
    summary_lines = []
    model.summary(print_fn=lambda x: summary_lines.append(x))
    return {
        "input_shape": str(model.input_shape),
        "output_shape": str(model.output_shape),
        "summary_top": "\n".join(summary_lines[:15]),
        "description": "CNN Binary Classifier (Good=0/Bad=1) on 4096x3 accelerometer data in g units."
    }
