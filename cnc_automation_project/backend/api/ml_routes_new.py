from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import os
import tensorflow as tf
import logging
from threading import Lock

logger = logging.getLogger(__name__)

WINDOW_SIZE = 4096
LSB_PER_G = 2048

router = APIRouter()

# Lazy model loading with lock
model = None
model_lock = Lock()
model_path = os.path.join(os.path.dirname(__file__), '..', 'saved_models', 'final_cnn_model.keras')

def load_model_safe():
    global model
    if model is None:
        with model_lock:
            if model is None:
                try:
                    logger.info(f"Loading model from {model_path}")\n                    model = tf.keras.models.load_model(model_path, compile=False, safe_mode=True)\n                    logger.info("Model loaded successfully with safe_mode")
                except Exception as e:
                    logger.error(f"Failed to load model: {e}")
                    raise RuntimeError(f"Model load failed: {str(e)}")
    return model


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
        
        # Lazy load model
        mdl = load_model_safe()
        
        prob_bad = mdl.predict(input_array, verbose=0)[0][0]
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
    try:
        mdl = load_model_safe()
        summary_lines = []
        mdl.summary(print_fn=lambda x: summary_lines.append(x))
        return {
            "input_shape": str(mdl.input_shape),
            "output_shape": str(mdl.output_shape),
            "summary_top": "\n".join(summary_lines[:15]),
            "description": "CNN Binary Classifier (Good=0/Bad=1) on 4096x3 accelerometer data in g units."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model info failed: {str(e)}")
