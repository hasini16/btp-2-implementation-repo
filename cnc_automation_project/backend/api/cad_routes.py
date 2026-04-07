from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

# Import CAD modules
from cad_integration.sw_connection import SolidWorksConnection
from cad_integration.feature_recognition import FeatureRecognizer
from cad_integration.gcode_generator import CAMWorksIntegrator

router = APIRouter()

class CADRequest(BaseModel):
    file_path: str

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
