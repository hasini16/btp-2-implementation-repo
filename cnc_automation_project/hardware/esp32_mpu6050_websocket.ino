// ==== this is working ============
//#include <Wire.h>
// #include <LSM303AGR_ACC_Sensor.h>
// #include <LSM303AGR_MAG_Sensor.h>

// // I2C Pins for IndusBoard Coin V2
// #define I2C_SDA 8
// #define I2C_SCL 9

// LSM303AGR_ACC_Sensor Acc(&Wire);
// LSM303AGR_MAG_Sensor Mag(&Wire);

// void setup() {
//   // Serial initialization
//   Serial.begin(115200);
//   delay(2000); // Give the ESP32-S2 time to connect to USB
  
//   Serial.println("--- IndusBoard Coin V2 LSM303AGR Test ---");

//   // Initialize I2C with the specific pins for your board
//   Wire.begin(I2C_SDA, I2C_SCL); 

//   // Initialize Accelerometer
//   if (Acc.begin() == 0) {
//     Acc.Enable();
//     Acc.EnableTemperatureSensor();
//     Serial.println("Accelerometer Ready!");
//   } else {
//     Serial.println("Acc Init Failed. Check your library edits.");
//   }

//   // Initialize Magnetometer
//   if (Mag.begin() == 0) {
//     Mag.Enable();
//     Serial.println("Magnetometer Ready!");
//   } else {
//     Serial.println("Mag Init Failed. Check your library edits.");
//   }
// }

// void loop() {
//   int32_t acc[3];
//   int32_t mag[3];
//   float temp;  
//   Acc.GetAxes(acc);
//   Mag.GetAxes(mag);
//   Acc.GetTemperature(&temp);


//   // Print Accel: X, Y, Z
//   Serial.printf("ACC: %f, %f, %f | ", acc[0]*0.001, acc[1]*0.001, acc[2]*0.001);
  
//   // Print Mag: X, Y, Z
//   Serial.printf("MAG: %d, %d, %d\n", mag[0], mag[1], mag[2]);

//   Serial.printf("temp : %f\n",temp);

//   delay(300);
// }
// =============================================

// =============================================
#include <Wire.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h> // Ensure you have ArduinoJson library installed
#include <LSM303AGR_ACC_Sensor.h>
#include <LSM303AGR_MAG_Sensor.h>

// --- Wi-Fi Credentials ---
const char* ssid = "adhithya";          // Replace with your Wi-Fi Name
const char* password = "adhithya365";  // Replace with your Wi-Fi Password

// --- Server Configuration ---
// Your laptop's IP address and FastAPI port
const char* websocket_server = "10.16.52.246"; 
const uint16_t websocket_port = 8000;
const char* websocket_path = "/api/live-feed/ws"; 

// I2C Pins for IndusBoard Coin V2
#define I2C_SDA 8
#define I2C_SCL 9

LSM303AGR_ACC_Sensor Acc(&Wire);
LSM303AGR_MAG_Sensor Mag(&Wire);
WebSocketsClient webSocket;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 100; // Send data every 100ms (10Hz)

// WebSocket Event Handler
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.printf("[WSc] Disconnected!\n");
            break;
        case WStype_CONNECTED:
            Serial.printf("[WSc] Connected to url: %s\n", payload);
            break;
    }
}

void setup() {
  Serial.begin(115200);
  delay(2000); 
  
  Serial.println("--- IndusBoard Coin V2 WebSocket Streamer ---");

  // --- Initialize Sensors ---
  Wire.begin(I2C_SDA, I2C_SCL); 

  if (Acc.begin() == 0) {
    Acc.Enable();
    Acc.EnableTemperatureSensor();
    Serial.println("Accelerometer Ready!");
  } else {
    Serial.println("Acc Init Failed.");
  }

  if (Mag.begin() == 0) {
    Mag.Enable();
    Serial.println("Magnetometer Ready!");
  } else {
    Serial.println("Mag Init Failed.");
  }

  // --- Connect to Wi-Fi ---
  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi Connected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // --- Configure WebSocket Client ---
  webSocket.begin(websocket_server, websocket_port, websocket_path);
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000); // Try to reconnect every 5s if dropped
}

void loop() {
  webSocket.loop(); // Keep WebSocket connection alive

  // Non-blocking delay to send data at the specified interval
  if (millis() - lastSendTime >= sendInterval) {
    lastSendTime = millis();
    
    int32_t acc[3];
    float temp;  
    
    Acc.GetAxes(acc);
    // Acc.GetTemperature(&temp);

    // Convert raw ACC data (mg) to float (g) if needed, 
    // or keep raw depending on how you trained the model.
    float accX = acc[0] * 0.001;
    float accY = acc[1] * 0.001;
    float accZ = acc[2] * 0.001;

    // --- Build JSON Payload ---
    // We package the 4 features (Vib_X, Vib_Y, Vib_Z, Temp) into an array
    // This matches the [features] part of the (timesteps, features) shape
    StaticJsonDocument<200> doc;
    doc["accel_x"] = acc[0]; // raw mg for backend preprocess
    doc["accel_y"] = acc[1];
    doc["accel_z"] = acc[2];

    String jsonString;
    serializeJson(doc, jsonString);

    // Send it!
    if(webSocket.isConnected()){
      webSocket.sendTXT(jsonString);
      Serial.print("Sent: ");
      Serial.println(jsonString);
    }
  }
}
// =========================================================================



// #include <Wire.h>
// #include <LSM303AGR_ACC_Sensor.h>
// #include <LSM303AGR_MAG_Sensor.h>

// // I2C Pins for IndusBoard Coin V2
// #define I2C_SDA 8
// #define I2C_SCL 9

// LSM303AGR_ACC_Sensor Acc(&Wire);
// LSM303AGR_MAG_Sensor Mag(&Wire);

// void setup() {
//   Serial.begin(115200);
//   delay(2000); 
  
//   Serial.println("--- IndusBoard Coin V2: SI Units Mode ---");

//   Wire.begin(I2C_SDA, I2C_SCL); 

//   if (Acc.begin() == 0) {
//     Acc.Enable();
//     Serial.println("Accelerometer Ready!");
//   } else {
//     Serial.println("Acc Init Failed.");
//   }

//   if (Mag.begin() == 0) {
//     Mag.Enable();
//     Serial.println("Magnetometer Ready!");
//   } else {
//     Serial.println("Mag Init Failed.");
//   }
// }

// void loop() {
//   int32_t acc_raw[3];
//   // int32_t mag_raw[3];

//   // Get original axes data
//   Acc.GetAxes(acc_raw);
//   // Mag.GetAxes(mag_raw);

//   // --- SI UNIT CONVERSIONS ---
  
//   // Convert mg to m/s^2
//   float accX_si = acc_raw[0] ;
//   float accY_si = acc_raw[1] ;
//   float accZ_si = acc_raw[2] ;

//   // // Convert mGauss to microTesla (uT)
//   // float magX_si = mag_raw[0] * 0.1f;
//   // float magY_si = mag_raw[1] * 0.1f;
//   // float magZ_si = mag_raw[2] * 0.1f;

//   // Print Accel in m/s^2
//   Serial.print("ACC [m/s^2]: ");
//   Serial.print(accX_si, 3); Serial.print(", ");
//   Serial.print(accY_si, 3); Serial.print(", ");
//   Serial.print(accZ_si, 3);

//   // Print Mag in uT
//   // Serial.print(" | MAG [uT]: ");
//   // Serial.print(magX_si, 2); Serial.print(", ");
//   // Serial.print(magY_si, 2); Serial.print(", ");
//   // Serial.println(magZ_si, 2);

//   delay(500);
// }