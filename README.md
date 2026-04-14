# BTP-2 Implementation Repository: CNC Automation & Predictive Maintenance

Welcome to the BTP-2 Implementation codebase. This repository contains the full iteration history and final source code for a comprehensive **CNC Automation and Health Monitoring Platform**. 

The goal of this project was to establish an intelligent, full-stack workflow that connects automatic CAD/CAM processing to live machine telemetry leveraging predictive maintenance neural networks.

## 🚀 Project Journey & Accomplishments

Over the course of this repository's development, several critical milestones were achieved to bring this modular edge-computing system to life:

1. **Machine Learning Pipeline Development**
   - Engineered data parsing scripts to handle heavy, multi-gigabyte `.h5` files containing real-world sensor telemetry.
   - Built an automated model generation script (`generate_model.py`) to benchmark machine learning models using vibration and temperature data.
   - Solved severe Out-Of-Memory (OOM) crashing issues by implementing selective sample limits, bringing memory footprints down to acceptable limits for commodity hardware.
   - Designed a CNN-LSTM combination architecture capable of assessing high-frequency sensor readings and predicting the Remaining Useful Life (RUL) of CNC drill bits and bearings.
   - Dealt with severe `Keras` deserialization bugs triggered by environmental disparities spanning different Tensorflow distributions, utilizing a monkey-patching strategy to strip invalid `quantization_config` constraints at runtime.

2. **System Architecture & Sub-Modules Integration (`cnc_automation_project/`)**
   - Migrated to decoupled FastAPI + React + ESP32 stack for live predictive maintenance:
     - **Backend**: FastAPI w/ lazy-loaded CNN model for health preds & WS broadcast of ESP32 accel streams.
     - **Frontend**: React/Vite dashboard for real-time visualization & notifications (Recharts, hot-toast).
     - **Hardware**: ESP32-S2 w/ LSM303AGR accel streaming raw 3-axis data @10Hz via WiFi WS.

3. **UI/UX Expansion**
   - Transformed the React UI into a premium, glassmorphic dark-mode dashboard.
   - Integrated dynamic `react-hot-toast` notifications handling connection throttles to ensure UI performance isn't bogged down by rapid hardware telemetry streams mapping out anomalies.

## 📁 Repository Structure & Quick Start

### cd cnc_automation_project/

**1. Backend** (Python 3.10+):
```
cd backend
pip install -r requirements.txt
python app.py  # or uvicorn app:app --port 8000 --reload
```
- Access http://localhost:8000/docs (Swagger)

**2. Frontend** (Node 20+):
```
cd frontend
npm install
npm run dev  # localhost:5173 (Vite default)
```

**3. Hardware** (Arduino IDE):
- Upload `hardware/esp32_mpu6050_websocket.ino` to ESP32-S2.
- Update WiFi SSID/pass & backend IP (websocket_server = "YOUR_LAPTOP_IP").
- Monitor Serial @115200.

### Full Structure
- `CNC_Machining-main/`: Legacy prototypes.
- `cnc_automation_project/` (detailed files/functionalities below):
  [existing sub-bullets unchanged]
- `diagrams/`: Arch diagrams.
- `build.py` / `diagrams.py`: Utilities.

## 🛠️ Tech Stack & Dependencies

### Backend (`cnc_automation_project/backend/requirements.txt`)
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
tensorflow==2.18.0
pandas numpy pydantic python-multipart lime flask pywin32 joblib==1.4.2 dill==0.3.8
```

### Frontend (`cnc_automation_project/frontend/package.json`)
- React ^19.2.4, react-dom ^19.2.4, recharts ^3.8.1, react-hot-toast ^2.6.0, axios ^1.14.0, react-router-dom ^7.14.0
- Vite ^5.4.11, TypeScript ~5.9.3

### Hardware
- ESP32-S2 Arduino IDE, WebSocketsClient, ArduinoJson, LSM303AGR library (accel+mag)

**ML**: TensorFlow/Keras CNN (input: (1,4096,3) accel in g-units, output: bad_prob binary).

**Prerequisites**: Python 3.10+, Node 20+, Arduino IDE 2.x, IndusBoard Coin V2 (ESP32-S2 + LSM303AGR).

## 🏗️ Architecture & Data Flow
1. ESP32 reads LSM303AGR accel (raw mg) → JSON payload → WS POST to backend /api/live-feed/ws.
2. Backend broadcasts to React clients + buffers for ML.
3. Frontend: Live charts (Recharts) + API poll /api/ml/predict-health (POST 4096x3 sequence → {health_status, bad_probability}).
4. CNN: tf.keras load → predict on normalized g-units → threshold 0.5 for Good/Bad.

## 🔌 Key API Endpoints (localhost:8000)
- `POST /api/ml/predict-health`: `{raw_sequence: [[x1,y1,z1], ... 4096]}` → `{health_status: "Good", bad_probability: 0.23}`
- `GET /api/ml/model-info`: Model summary/shape.
- `WS /api/live-feed/ws`: Bidirectional; ESP32 producer, React consumers.

---

*Evolution from data exploration to production-ready IIoT predictive maintenance platform.*
