import { useState, useEffect } from "react";
import API from "../api/api";

export default function OpenClawRPSChart() {
  const [history, setHistory] = useState([]);
  const [rps, setRps] = useState(0);
  const [errorRate, setErrorRate] = useState(0);

  useEffect(() => {
    const load = () => {
      API.get("/system/openclaw-rps").then(res => {
        setHistory(res.data.history);
        setRps(res.data.rps.toFixed(2));
        setErrorRate(res.data.error_rate.toFixed(1));
      });
    };

    load();
    const interval = setInterval(load, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "1rem", background: "#eef", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>OpenClaw Request‑Per‑Second</h2>

      <p><strong>RPS:</strong> {rps}</p>
      <p><strong>Error Rate:</strong> {errorRate}%</p>

      <div style={{ display: "flex", gap: "2px", height: "80px", alignItems: "flex-end" }}>
        {history.map((h, i) => {
          const height = Math.min(80, h.duration * 300); // scale duration
          const color = h.status >= 400 ? "#ff4444" : "#44ff44";

          return (
            <div
              key={i}
              style={{
                width: "4px",
                height: `${height}px`,
                background: color
              }}
            />
          );
        })}
      </div>
    </div>
  );
}
