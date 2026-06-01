import { useState, useEffect } from "react";
import API from "../api/api";

export default function OpenClawPlannerBrain() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const load = () => {
      API.get("/system/planner-brain").then(res => setData(res.data));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  if (!data) return null;

  return (
    <div style={{ padding: "1rem", background: "#fff0f5", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>Planner Brain — What It’s Doing & Why</h2>
      <p><strong>Turbo mode:</strong> {data.turbo_mode ? "ON" : "OFF"}</p>
      <p><strong>Auto‑triggered:</strong> {data.auto_triggered ? "Yes" : "No"}</p>
      <p><strong>Auto turbo activations:</strong> {data.auto_turbo_activations}</p>
      <p><strong>Last auto turbo at:</strong> {data.last_auto_turbo_at ? new Date(data.last_auto_turbo_at * 1000).toLocaleTimeString() : "never"}</p>

      <h3 style={{ marginTop: "0.75rem" }}>Per‑Path Behavior</h3>
      <pre style={{ fontSize: "12px", maxHeight: "200px", overflow: "auto" }}>
        {Object.entries(data.agents || {}).map(([path, info]) =>
          `${path} — calls=${info.calls}, err=${info.error_rate?.toFixed(1)}%, avg=${info.avg_ms?.toFixed(1)}ms, last_auto_turbo=${info.last_auto_turbo ? new Date(info.last_auto_turbo * 1000).toLocaleTimeString() : "never"}\n`
        )}
      </pre>
    </div>
  );
}
