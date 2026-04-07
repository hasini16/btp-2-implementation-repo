# CNC Automation Web System

This module contains the actively developed full-stack application for the CNC Automation and Predictive Maintenance system. It is decoupled into three primary folders for logical separation of concerns: Backend (API), Frontend (UI), and Hardware (Edge IoT).

## 🗂️ Project Layout

### 1. Backend (`/backend`)
The backend is driven by **FastAPI**. It handles two main responsibilities: serving predictions from the trained CNN-LSTM model and managing real-time WebSocket telemetry.

- **Stack**: Python, FastAPI, TensorFlow/Keras.
- **Key Routes**:
  - `POST /api/ml/predict-rul`: Pass an array of `[50, 4]` shaped sensor matrices to get back an instantaneous health rating and RUL (Remaining Useful Life) in hours.
  - `WS /api/live-feed/ws`: Hook an ESP32 into this websocket to stream `accel_x, accel_y, ...` data points directly to connected frontend clients.
- **Run the Server**:
  ```bash
  cd backend
  source venv/bin/activate  # Ensure you are using the venv!
  uvicorn app:app --reload --port 8000
  ```
  *Swagger UI tests available at `http://localhost:8000/docs`.*

### 2. Frontend (`/frontend`)
The UI is built with **React** via **Vite**. It heavily features ReCharts for hardware data visualization, and `react-hot-toast` for system notifications, all wrapped in a custom glassmorphic CSS aesthetic.

- **Stack**: React (TypeScript), Vite, Tailwind-like raw CSS, Recharts.
- **Run the Dashboard**:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
  *Runs locally on port `5173`. Includes CAD automation simulation endpoints and a Machine Health portal connected to the backend.*

### 3. Hardware (`/hardware`)
The edge device source code designed to be flashed directly to an ESP32 controller. 

- Requires an MPU6050 sensor hooked via I2C (`SDA`, `SCL`).
- **Functionality**: Reads gyro and accelerometer values at a high polling rate and dispatches JSON packets to the backend WebSocket pipeline.
- Flash using **Arduino IDE** or **PlatformIO**.

## 🔌 Connection Flow
1. The **ESP32** powers on, connects to WiFi, and opens a WebSocket to `ws://127.0.0.1:8000/api/live-feed/ws`.
2. The **FastAPI Backend** acts as a bridge, ingesting these 6-axis hardware arrays.
3. The **React Frontend** opens a socket to the same backend. The backend bounces the telemetry to the dashboard line charts.
4. If the UI requests a prediction, the Backend passes a 50-tick sequence to `saved_models/cnn_lstm_rul.keras` to calculate real-time tool deterioration.
