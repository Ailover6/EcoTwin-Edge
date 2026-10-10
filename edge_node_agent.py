import time
import random
import requests

SERVER_URL = "http://localhost:8000/api/edge/telemetry"
NODE_ID = "zone_A_rooftop"

def simulate_edge_sensor_loop():
    print(f"Starting Edge AI Node agent for {NODE_ID}...")
    while True:
        # Simulate sensor readings (Replace with OpenCV thermal frame analysis or DHT22/Soil pins)
        surface_temp = round(random.uniform(40.0, 48.5), 1)
        ambient_temp = round(random.uniform(36.0, 40.0), 1)
        soil_moisture = round(random.uniform(18.0, 50.0), 1)
        tank_storage = 1200.0
        anomaly = True if surface_temp > 44.0 else False

        payload = {
            "node_id": NODE_ID,
            "surface_temp_c": surface_temp,
            "ambient_temp_c": ambient_temp,
            "soil_moisture_percent": soil_moisture,
            "tank_storage_liters": tank_storage,
            "thermal_anomaly_detected": anomaly
        }

        try:
            response = requests.post(SERVER_URL, json=payload)
            print(f"[Telemetry Sent] Surface: {surface_temp}°C | Anomaly: {anomaly} | Response: {response.json()}")
        except Exception as e:
            print(f"Connection error to FastAPI core: {e}")

        time.sleep(5)

if __name__ == "__main__":
    simulate_edge_sensor_loop()