from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import the router from your api folder
from api.routes import router as api_router

app = FastAPI(
    title="CNC Automation & Predictive Maintenance API",
    description="Backend for bridging SolidWorks/CAMWorks and CNN-LSTM models.",
    version="1.0.0"
)

# Configure CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000" , "*"], # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routes
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "API is running. Access /docs for the Swagger UI."}

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run("app:app", port=8000, reload=True)