# Machine Health Remote Monitoring System

Pure web app for ESP32S2 Indusboard V2 machine health monitoring with CNN predictions.

## Quick Start

1. **Backend** (port 8000)
   ```
   cd cnc_automation_project/backend
   python -m venv venv
   venv\\Scripts\\activate
   pip install -r requirements.txt
   uvicorn app:app --reload --port 8000
   ```
   API docs: http://localhost:8000/docs

2. **Frontend** (port 5173)
   ```
   cd cnc_automation_project/frontend
   npm install
   npm run dev
   ```
   Open http://localhost:5173

3. **Hardware** Flash `hardware/esp32_indusboard_ws.ino` to ESP32S2 Indusboard V2 Coin (Arduino IDE)

## Features
- Live WS telemetry accel raw/g charts/table
- Rolling buffer 4096 samples
- CNN binary Good/Bad prediction on-demand
- Model metrics cards
- Connection/machine status
- Full logs/debug panel
- Responsive glassmorphic UI

## Connection Flow
ESP32S2 → raw accel mg over WS → Backend broadcast → Frontend buffer/charts → Predict sends 4096x3 raw mg → Backend /1000 reshape predict → Result cards/logs

Swagger: POST /api/ml/predict-health {raw_sequence: [[raw_mgx1, mgy1, mgz1], ... 4096]} 
GET /api/ml/model-info

Done! 🎉
