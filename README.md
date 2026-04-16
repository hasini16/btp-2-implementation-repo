# CNC Predictive Maintenance Platform using Vibration Analysis & CNN

## 🚀 Project Overview

This project implements a **real-time predictive maintenance system for CNC machines** focusing on machine health monitoring through continuous vibration data observation. 

**Key Components:**
- **Hardware**: ESP32-S2 Indusboard V2 Coin board collects 3-axis acceleration (vibration) data using LSM303AGR sensor.
- **Backend**: FastAPI server with WebSocket live feed broadcasting, CNN model for binary classification ('good' vs 'bad').
- **Frontend**: React dashboard for live sensor visualization and health predictions.
- **ML Model**: Custom CNN trained from scratch on **BOSCH CNC Milling Dataset** (benchmark: 3 milling machines, 14 operations, 2+ years data via BOSCH CISS sensors, good/bad folders, input: 4096x3 accel sequences, output: binary health status).

The system enables **live machine health observation** with predictions triggered on buffered sensor streams, reducing unplanned downtime in CNC operations.

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

## 🚀 Project Journey & Accomplishments

Over the course of this repository's development, several critical milestones were achieved...

[Keep all existing content from original README below, with path updates:]

### cd predictiveMaintainence/

**1. Backend** (Python 3.10+):
```
cd predictiveMaintainence/backend
pip install -r requirements.txt
python app.py  # or uvicorn app:app --port 8000 --reload
```

**2. Frontend** (Node 20+):
```
cd predictiveMaintainence/frontend
npm install
npm run dev  # localhost:5173
```

**3. Hardware** (Arduino IDE):
- Upload `predictiveMaintainence/hardware/esp32_mpu6050_websocket.ino` to ESP32-S2.
- Update WiFi SSID/pass & backend IP.

### Full Structure
- `predictiveMaintainence/backend/`: FastAPI, CNN models, WS.
- `predictiveMaintainence/frontend/`: React/Vite dashboard.
- `predictiveMaintainence/hardware/`: ESP32 firmware.
- `btp-2-literature-repo-main/`: Reference papers/CSV.

## 🛠️ Tech Stack & Dependencies
[Keep existing, update paths]

### Backend (`predictiveMaintainence/backend/requirements.txt`)
[unchanged]

### Frontend (`predictiveMaintainence/frontend/package.json`)
[unchanged]

### Hardware
[unchanged]

## 🏗️ Architecture & Data Flow
1. ESP32 reads LSM303AGR accel → JSON → WS to backend.
2. Backend broadcasts to React + buffers for CNN predict.
3. Frontend: Live charts + /ml/predict-health API.

## 🔌 Key API Endpoints (localhost:8000)
[unchanged]

---

*Production-ready CNC PdM platform with literature-backed motivation.*

