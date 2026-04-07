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
   - Migrated from disparate scripts to a clean, decoupled architecture:
     - **Backend**: A FastAPI server handling ML inference and WebSocket bridging.
     - **Frontend**: A React/Vite dashboard allowing users to visualize CAD processes and live server data.
     - **Hardware**: An ESP32 / MPU6050 microcontroller schema transmitting 6-axis gyro/accelerometer data to the server via WebSockets.

3. **UI/UX Expansion**
   - Transformed the React UI into a premium, glassmorphic dark-mode dashboard.
   - Integrated dynamic `react-hot-toast` notifications handling connection throttles to ensure UI performance isn't bogged down by rapid hardware telemetry streams mapping out anomalies.

## 📁 Repository Structure

- `CNC_Machining-main/`: Contains older prototype testing data and monolithic scripts.
- `cnc_automation_project/`: The **primary working directory**. Contains the clean split of `backend`, `frontend`, and `hardware` logic. (See its dedicated `README.md` for run instructions).
- `diagrams/`: Contains generated architecture sequence charts.
- `build.py` / `diagrams.py`: Historical utility scripts mapped at the root.

## 🛠️ Global Tech Stack overview

- **ML & Data Processing**: Python, TensorFlow, Keras, NumPy, H5py
- **Backend API**: FastAPI, Uvicorn, WebSockets
- **Frontend Dashboard**: React (TypeScript), Vite, Recharts, React-Hot-Toast
- **Edge Hardware Integration**: ESP32 (C++ / Arduino IDE), MPU6050 Accelerometer

---

*This repository documents the evolution from raw data exploration to a stable, networked Industrial IoT (IIoT) dashboard ready for testing.*
