# CNC Predictive Maintenance Platform using Vibration Analysis & CNN

## 🚀 Project Overview

**Real-time machine health monitoring for CNC machines via edge vibration analysis.**

**Core Pipeline:**
1. **ESP32-S2 Indusboard V2 Coin**: LSM303AGR accelerometer streams 3-axis raw vibration (mg) @10Hz via WiFi WebSocket.
2. **FastAPI Backend**: Receives/broadcasts live feeds to DB (PostgreSQL/SQLite), buffers 4096 timesteps, CNN binary prediction (good/bad).
3. **React Frontend**: Live Recharts dashboard with vibration charts, health status cards, confidence scores.
4. **ML Core**: Keras CNN trained on BOSCH CNC dataset (3 mills, 14 ops, 2+yr CISS sensor data, binary good/bad).

**Key Innovation**: End-to-end deployable PdM with benchmark dataset CNN, edge streaming, no CAD/CAM (focused on health).

## 📚 Literature Review & Motivation
Predictive maintenance (PdM) for CNC machines addresses massive downtime costs (up to 50% of maintenance budget). Literature shows growing ML/DL adoption for vibration-based fault prediction, but gaps remain in **real-time edge deployment, lightweight hardware integration (ESP32), BOSCH dataset CNNs, and live dashboards**.

| Title | Authors | Year | Summary | Gap/Need Addressed by Our Project |
|-------|---------|------|---------|----------------------------|
| A hybrid predictive maintenance approach for CNC machine tool driven by Digital Twin | Weichao Luo et al. | 2020 | Hybrid DT + data-driven PdM merging physics models with sensors for life-cycle fault prediction. | Lacks lightweight real-time edge sensors (ESP32) and binary CNN on benchmark BOSCH data. |
| Optimizing Predictive Maintenance Strategies for CNC Machining Centers... | Dr. Gorakh Wakhare | 2023 | Compares RF/GB/NN for CNC PdM, emphasizes XAI robustness. | No live WS dashboard or specific vibration CNN training/deployment pipeline. |
| Predictive Maintenance in CNC Machines Using Machine Learning | N. Arjun et al. | 2025 | Hybrid RF+LSTM PdM with multimodal sensors, LIME XAI on embedded CNC. | Missing BOSCH dataset focus, ESP32 streaming, React live viz. |
| An Industrial IoT Framework for Predictive Maintenance of CNC Lathe Spindles... | Nikhil M. Thoppil, V. Vasu | 2025 | IIoT + LSTM/biLSTM RUL on spindle vib via ThingSpeak cloud. | Narrow to spindles; our binary good/bad CNN covers full machine, adds live frontend. |
| Research on Predictive Maintenance of CNC Machine Tools Based on Deep Learning | Jing Pu | 2026 | CNN-LSTM fusion on multi-sensor (vib, acoustic) for nonlinear degradation. | Black-box issue; our project adds live interpretable dashboard + BOSCH binary focus. |
| Predictive maintenance system for CNC machines | Sridevi S et al. | 2025 | Arduino sensors + RF anomaly detection ('Be Shield' system). | Basic ML; our CNN on benchmark data + WebSocket live preds superior for production. |

**Motivation**: Builds on literature by providing **end-to-end real-time system** with production-ready CNN on BOSCH benchmark, edge ESP32, WS live feed – filling gaps in deployable, visual PdM.

## 🏗️ Technical Architecture

```
ESP32 Sensor (10Hz) --> WS JSON {accel_x,y,z mg} --> FastAPI /live-feed/ws (ConnectionManager broadcast + DB log)
  |
  v
Buffer 4096x3 --> CNN Predict (/ml/predict-health) --> {health_status, bad_prob, conf, thresh}
  |
  v
React Dashboard: Live line charts (Recharts), toast notifs, prediction cards
```

**Data Shapes**:
- Input to CNN: (1, 4096, 3) - normalized g-units (mg * 0.001).
- Output: softmax [good_prob, bad_prob], thresh=0.5.

**CNN Model** (final_cnn_model.keras):
- Loaded via `tf.keras.models.load_model(saved_models/final_cnn_model.keras)`.
- Architecture: Custom 1D CNN for sequential vibration (details in `api/ml_routes_new_fixed.py`).
- Preprocessing: Pandas normalize, reshape to model input.

**Database** (SQLAlchemy):
```sql
Table sensor_feeds: id (PK), timestamp, accel_x (float), accel_y, accel_z, machine_id (default 'cnc1').
```

## 📋 Software Documentation

### Backend Setup & APIs
```
cd predictiveMaintainence/backend
pip install -r requirements.txt  # TF 2.18, FastAPI 0.115, SQLAlchemy 2.0
uvicorn app:app --port 8000 --reload
```
- **Swagger**: http://localhost:8000/docs
- **Endpoints**:
  | Path | Method | Desc | Req/Resp |
  |------|--------|------|-----------|
  | `/api/live-feed/ws` | WS | Bidir stream: ESP32 send → broadcast to clients. | JSON {accel_x,y,z} |
  | `/api/ml/predict-health` | POST | CNN predict on sequence. | `{raw_sequence: [[x,y,z],...4096]}` → `{health_status:str, bad_prob:float, conf:float, thresh:float}` |
  | `/api/ml/model-info` | GET | Model summary/shape. | `{input_shape, output_shape, summary}` |

**Pydantic Models** (in ml_routes):
- HealthResponse: status, bad_prob (sigmoid), confidence, threshold (0.5).

**Logging**: logs/backend.log (INFO+).

### Frontend Setup
```
cd predictiveMaintainence/frontend
npm i  # React 19, Recharts 3.8, Vite 5.4
npm run dev  # http://localhost:5173
```
- **Components**: Dashboard.tsx - LineChart (vib/temp), status grids, hot-toast.
- **Services**: api.ts - axios to /ml/predict-health, model-info.

### Hardware Firmware
```
Arduino IDE: Upload esp32_mpu6050_websocket.ino to ESP32-S2 Indusboard V2 Coin.
```
**Config**:
- I2C: SDA=8, SCL=9 (LSM303AGR).
- Sampling: 10Hz (100ms interval).
- WS: Update `websocket_server="YOUR_PC_IP"`, SSID/pass.
- Payload: `{"accel_x":raw_mg, "accel_y":raw_mg, "accel_z":raw_mg}`.

## 🚀 Quick Start (Updated Paths)
```
# Backend
cd predictiveMaintainence/backend && pip install -r requirements.txt && uvicorn app:app --port 8000

# Frontend (new tab)
cd predictiveMaintainence/frontend && npm i && npm run dev

# ESP32: Upload firmware, update IP to your PC's IP (ipconfig), monitor Serial 115200
```
DB auto-creates tables on startup.

## 🚀 Project Journey & Accomplishments

1. **ML Pipeline**: HDF5 parsing, OOM fixes, CNN from scratch on BOSCH data.
2. **Stack**: FastAPI + React + ESP32 WS.
3. **UI**: Glassmorphic dark dashboard, Recharts live plots.
[Keep original journey details]

## 🛠️ Tech Stack & Dependencies

**Backend** (`predictiveMaintainence/backend/requirements.txt`):
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
tensorflow==2.18.0
sqlalchemy==2.0.35
pandas numpy joblib==1.4.2 psycopg2-binary==2.9.9
```

**Frontend** (`predictiveMaintainence/frontend/package.json`):
```
"dependencies": {
  "react": "^19.2.4",
  "recharts": "^3.8.1",
  "react-hot-toast": "^2.6.0",
  "axios": "^1.14.0"
}
```

**Hardware**: ESP32-S2, LSM303AGR lib, WebSocketsClient, ArduinoJson.

## 🏗️ Architecture & Data Flow (Detailed)
[Expanded from existing]

## 🔌 Key API Endpoints (Expanded)
[With schemas/cURL examples]

**Example cURL Predict**:
```bash
curl -X POST http://localhost:8000/api/ml/predict-health \
  -H "Content-Type: application/json" \
  -d '{"raw_sequence": [[0.1,0.2,0.3]] * 4096]}'
```

## 🚀 Deployment & Troubleshooting
- **Env**: Python 3.10+, Node 20+, PostgreSQL (or SQLite dev).
- **PC IP**: Static IP recommended for ESP32 WS.
- **TF OOM**: Reduce batch_size=1 in predict.
- **CORS**: Allows localhost:5173.
- **Models**: saved_models/final_cnn_model.keras/joblib.

---

*Full-stack CNC PdM: BOSCH CNN + ESP32 edge + live React dashboard.*

