from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import the routers from api folder
from api.cad_routes import router as cad_router
from api.ml_routes import router as ml_router
from api.live_feed_routes import router as live_feed_router

app = FastAPI(
    title="CNC Automation & Predictive Maintenance API",
    description="Backend for bridging SolidWorks/CAMWorks and CNN-LSTM models.",
    version="1.0.0"
)

# Configure CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"], # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routes
app.include_router(cad_router, prefix="/api/cad", tags=["CAD Automation"])
app.include_router(ml_router, prefix="/api/ml", tags=["Machine Health"])
app.include_router(live_feed_router, prefix="/api/live-feed", tags=["Live Feed"])

@app.get("/")
async def root():
    return {"message": "API is running. Access /docs for the Swagger UI."}

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run("app:app", port=8000, reload=True)