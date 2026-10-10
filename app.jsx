import React, { useState, useEffect } from 'react';

export default function App() {
  const [twinData, setTwinData] = useState(null);

  useEffect(() => {
    const fetchTwin = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/digital-twin/state');
        const json = await res.json();
        setTwinData(json);
      } catch (err) {
        console.error("Failed to sync digital twin state", err);
      }
    };
    fetchTwin();
    const interval = setInterval(fetchTwin, 3000);
    return () => clearInterval(interval);
  }, []);

  if (!twinData) return <div className="min-h-screen bg-slate-950 text-white p-8">Loading Spatial Digital Twin...</div>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 font-sans">
      <header className="max-w-6xl mx-auto mb-8 border-b border-slate-800 pb-4">
        <h1 className="text-3xl font-extrabold text-cyan-400">EcoTwin-Edge: Spatial Thermal & Water Matrix</h1>
        <p className="text-slate-400 text-sm">Combined Edge-AI Thermal Vision & Microclimate Digital Twin</p>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        {Object.entries(twinData.nodes).map(([id, node]) => (
          <div key={id} className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-xl flex flex-col justify-between">
            <div>
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-slate-200 uppercase tracking-wider">{node.node_id}</h2>
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${node.thermal_anomaly_detected ? 'bg-red-900 text-red-300 animate-pulse' : 'bg-emerald-900 text-emerald-300'}`}>
                  {node.thermal_anomaly_detected ? '🔥 Thermal Anomaly' : '✅ Stable'}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-slate-800 p-3 rounded-lg">
                  <span className="text-xs text-slate-400">Surface Temp</span>
                  <div className="text-2xl font-extrabold text-orange-400">{node.surface_temp_c}°C</div>
                </div>
                <div className="bg-slate-800 p-3 rounded-lg">
                  <span className="text-xs text-slate-400">Soil Moisture</span>
                  <div className="text-2xl font-extrabold text-emerald-400">{node.soil_moisture_percent}%</div>
                </div>
                <div className="bg-slate-800 p-3 rounded-lg">
                  <span className="text-xs text-slate-400">Tank Storage</span>
                  <div className="text-2xl font-extrabold text-sky-400">{node.tank_storage_liters} L</div>
                </div>
                <div className="bg-slate-800 p-3 rounded-lg">
                  <span className="text-xs text-slate-400">Heat Stress Window</span>
                  <div className="text-2xl font-extrabold text-red-400">{node.predicted_heat_stress_hours} hrs</div>
                </div>
              </div>
            </div>

            <div className="bg-slate-800 p-4 rounded-lg flex items-center justify-between">
              <div>
                <span className="text-xs text-slate-400 block">Greywater Cascade Actuator</span>
                <span className="text-sm font-semibold text-slate-200">{node.mister_cascade_status}</span>
              </div>
              <div className={`w-3 h-3 rounded-full ${node.mister_cascade_status === 'ACTIVE_CASCADE' ? 'bg-cyan-400 animate-ping' : 'bg-slate-600'}`}></div>
            </div>
          </div>
        ))}
      </main>
    </div>
  );
}