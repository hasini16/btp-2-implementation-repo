import requests
import json
import numpy as np

# Generate random mock data for the test (1 sequence of 50 timesteps, with 4 features each)
# Features: [accel_x, accel_y, accel_z, temperature]
dummy_sequence = np.random.rand(50, 4).tolist()

payload = {
    "sequence_data": dummy_sequence
}

url = "http://127.0.0.1:8000/api/ml/predict-rul"
headers = {"Content-Type": "application/json"}

print(f"Sending POST request to {url} with 50 timesteps...")
try:
    response = requests.post(url, json=payload, headers=headers)
    print("\n--- Response ---")
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=4))
except requests.exceptions.ConnectionError:
    print("Failed to connect. Is the Uvicorn server running on port 8000?")
