import { useState, useEffect } from "react";
import API from "../api/api";

export default function OpenClawErrorHeatmap() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const load = () => {
      API.get("/system/openclaw-rps").then(res => {
        setHistory(res.data.history || []);
      });
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  const now = Date.now();
  const buckets = Array.from({ length: 24 }, (_, i) => {
    const cutoff = now - (i + 1) * 3600 * 1000;
    const count = history.filter(h => {
      const t = h.timestamp * 1000;
      return t > cutoff && h.status >= 400;
    }).length;
    return count;
  });

  return (
    <div style={{ padding: "1rem", background: "#f0f0ff", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>Error Heatmap (Last 24h)</h2>
      <div style={{ display: "flex", gap: "4px" }}>
        {buckets.map((c, i) => {
          const intensity = Math.min(c, 5);
          const color = intensity === 0 ? "#e0e0e0" : `rgba(255,0,0,${0.2 + intensity * 0.15})`;
          return (
            <div
              key={i}
              style={{
                width: "20px",
                height: "20px",
                background: color,
                borderRadius: "4px",
              }}
              title={`${24 - i}h ago: ${c} errors`}
            />
          );
        })}
      </div>
    </div>
  );
}
