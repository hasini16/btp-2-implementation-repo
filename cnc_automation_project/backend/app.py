from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from database import Base, engine
from models import Base as ModelsBase  # Avoid name conflict

# Import the routers from api folder
# CAD removed: from api.cad_routes import router as cad_router
from api.ml_routes_new_fixed import router as ml_router
from api.live_feed_routes import router as live_feed_router

app = FastAPI(
    title="Machine Health Remote Monitoring API",
    description="FastAPI backend for ESP32S2 live telemetry and CNN health predictions.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    # Create tables if not exist
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/initialized.")

# Configure CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"], # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routes
# CAD removed: app.include_router(cad_router, prefix="/api/cad", tags=["CAD Automation"])
app.include_router(ml_router, prefix="/api/ml", tags=["ML Predictions"])
app.include_router(live_feed_router, prefix="/api/live-feed", tags=["Live Feed"])

@app.get("/")
async def root():
    return {"message": "API is running. Access /docs for the Swagger UI."}

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run("app:app", port=8000, reload=True)