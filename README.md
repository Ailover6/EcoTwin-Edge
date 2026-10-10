# 💧 Autonomous Smart Water Tank & Distribution Scheduling System
*Built for WeMakeDevs Environmental Hacks (Heat and Water Track)*


## 📌 1. The Problem
Urban water management faces severe inefficiencies:
* **Tank Overflows & Pump Burnouts:** Lack of real-time monitoring leads to constant overflows and damaged equipment.
* **Massive Daily Water Wastage:** Millions of liters of potable water are wasted due to manual oversight.
* **High Energy Consumption:** Unoptimized pumping schedules increase energy demand and carbon footprint.

---

## 🛠️ 2. The Build
An autonomous end-to-end water management system featuring real-time telemetry, predictive scheduling, and automated control.

* **Frontend:** React Dashboard (Real-time monitoring, WebSocket connection, manual/auto toggle).
* **Backend:** Python & FastAPI (Processes sensor data, executes scheduling logic, API endpoints).
* **Cloud/IoT:** AWS IoT Core, Docker containerization, and AWS ECS/Fargate deployment.

### Key Features:
1. **Real-Time Monitoring:** Live water level visualization and telemetry status updates.
2. **Predictive Scheduling:** Demand forecasting to run pumps during optimal hours.
3. **Automated Control:** Threshold-based safety automation to prevent overflows and dry runs.
4. **Instant Alerts:** Notification system via AWS SNS/SES for critical anomalies.

---

## ☁️ 3. Where AWS Fits
* **Compute & Hosting:** AWS EC2 / ECS (Fargate) hosts the FastAPI backend securely and reliably.
* **Data & Storage:** Amazon RDS / DynamoDB manages historical telemetry data and user configurations.
* **IoT & Integration:** AWS IoT Core handles edge sensor data streams.
* **Cost Optimization:** Designed entirely using AWS Free Tier eligible services ($200 free trial usage).

---

## 🚀 Getting Started & Local Setup

### Prerequisites
* Python 3.10+
* Node.js & npm
* Docker

### Installation & Run
1. Clone the repository:
   ```bash
   git clone [https://github.com/Ailover6/EcoTwin-Edge.git](https://github.com/Ailover6/EcoTwin-Edge.git)
   cd EcoTwin-Edge
