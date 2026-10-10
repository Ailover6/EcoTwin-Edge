from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import datetime
import random

app = FastAPI(title="EcoTwin-Edge 24H Predictive Engine", version="7.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory event log store
system_event_log = []

def log_event(city_name, description):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S %d-%m")
    event = {"timestamp": timestamp, "city": city_name, "event": description}
    system_event_log.insert(0, event)
    if len(system_event_log) > 50:
        system_event_log.pop()

last_city_state = None

@app.get("/api/city/search")
async def search_city_weather(q: str):
    global last_city_state
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://wttr.in/{q}?format=j1"
            response = await client.get(url, timeout=5.0)
            
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="City not found.")
            
            data = response.json()
            current = data["current_condition"][0]
            
            ambient_temp = float(current["temp_C"])
            surface_temp = round(ambient_temp + (3.5 if ambient_temp < 30 else 5.0), 1)
            is_stressed = surface_temp > 35.0

            # 24-Hour Forecast model (range 1 to 25 hours)
            forecast_temps = []
            forecast_times = []
            now = datetime.datetime.now()
            
            for i in range(1, 25):
                future_hour = now + datetime.timedelta(hours=i)
                forecast_times.append(future_hour.strftime("%I %p"))
                
                # Solar progression simulation curve over 24 hours
                solar_curve = max(0, 1.0 - abs(14 - future_hour.hour) / 8)
                predicted_temp = round(ambient_temp + (6 * solar_curve), 1)
                forecast_temps.append(predicted_temp)

            current_status = "STRESSED" if is_stressed else "NORMAL"
            if last_city_state and last_city_state["region_name"] == q.capitalize():
                if last_city_state["status"] != current_status:
                    if current_status == "STRESSED":
                        log_event(q.capitalize(), "CRITICAL: Thermal threshold exceeded. Actuators engaged.")
                    else:
                        log_event(q.capitalize(), "INFO: Microclimate stabilized. System on standby.")
            
            last_city_state = {"region_name": q.capitalize(), "status": current_status}

            city_node = {
                "node_id": f"{q.capitalize()} - Edge Node",
                "region_name": q.capitalize(),
                "ambient_temp_c": ambient_temp,
                "surface_temp_c": surface_temp,
                "soil_moisture_percent": round(max(15.0, 80.0 - (ambient_temp * 1.2)), 1),
                "tank_storage_liters": round(2500.0 - (random.uniform(10, 50) if is_stressed else 0), 1),
                "thermal_anomaly_detected": is_stressed,
                "mister_cascade_status": "ACTIVE_CASCADE" if is_stressed else "STANDBY",
                "predicted_heat_stress_hours": max(2.0, round(20.0 - (ambient_temp * 0.4), 1)),
                "forecast_labels": forecast_times,
                "forecast_data": forecast_temps
            }
            
            return {
                "timestamp": datetime.datetime.now().isoformat(),
                "searched_city": city_node,
                "event_log": system_event_log
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))