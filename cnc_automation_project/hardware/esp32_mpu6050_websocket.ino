#include <WiFi.h>
#include <WebSocketsClient.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Wi-Fi Credentials
const char* ssid     = "adhithya";
const char* password = "adhithya365";

// WebSocket Server URL (Assuming backend runs locally on same network, please replace with actual backend IP!)
// For testing locally, if your laptop IP is 192.168.x.x, place it below.
const char* websocket_server = "192.168.1.100";  
const uint16_t websocket_port = 8000;
const char* websocket_path = "/api/live-feed/ws"; 

WebSocketsClient webSocket;
Adafruit_MPU6050 mpu;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 100; // Send data every 100ms (10Hz)

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      Serial.println("[WS] Disconnected!");
      break;
    case WStype_CONNECTED:
      Serial.printf("[WS] Connected to url: %s\n", payload);
      break;
    case WStype_TEXT:
      Serial.printf("[WS] Message from Server: %s\n", payload);
      break;
  }
}

void setup() {
  Serial.begin(115200);
  
  // Custom I2C pins for MPU6050
  Wire.begin(21, 22);

  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Connect to Wi-Fi
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Establish WebSocket connecton
  webSocket.begin(websocket_server, websocket_port, websocket_path);
  webSocket.onEvent(webSocketEvent);
  
  // Reconnect automatically
  webSocket.setReconnectInterval(5000);
}

void loop() {
  webSocket.loop();

  // Send data periodically Without blocking (delay)
  if (millis() - lastSendTime >= sendInterval) {
    lastSendTime = millis();
    
    if (webSocket.isConnected()) {
      sensors_event_t a, g, temp;
      mpu.getEvent(&a, &g, &temp);

      // We compose a simple JSON payload with Acceleration and Gyro values
      String jsonPayload = "{";
      jsonPayload += "\"accel_x\":" + String(a.acceleration.x) + ",";
      jsonPayload += "\"accel_y\":" + String(a.acceleration.y) + ",";
      jsonPayload += "\"accel_z\":" + String(a.acceleration.z) + ",";
      jsonPayload += "\"gyro_x\":" + String(g.gyro.x) + ",";
      jsonPayload += "\"gyro_y\":" + String(g.gyro.y) + ",";
      jsonPayload += "\"gyro_z\":" + String(g.gyro.z) + ",";
      jsonPayload += "\"temperature\":" + String(temp.temperature);
      jsonPayload += "}";

      webSocket.sendTXT(jsonPayload);
      // Serial.println("Sent: " + jsonPayload); // Uncomment to debug
    }
  }
}
