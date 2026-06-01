import { useState, useEffect } from "react";
import API from "../api/api";

export default function OpenClawMonitor() {
  const [stats, setStats] = useState({
    cpu: 0,
    ram: 0,
    uptime_seconds: 0,
    crashes_last_24h: 0,
    crash_timestamps: []
  });

  useEffect(() => {
    const load = () => {
      API.get("/system/openclaw-stats").then(res => setStats(res.data));
    };

    load();
    const interval = setInterval(load, 2000);
    return () => clearInterval(interval);
  }, []);

  const uptime = new Date(stats.uptime_seconds * 1000)
    .toISOString()
    .substr(11, 8);

  return (
    <div style={{ padding: "1rem", background: "#ddeeff", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>OpenClaw Live Monitor</h2>

      <p><strong>CPU:</strong> {stats.cpu}%</p>
      <p><strong>RAM:</strong> {stats.ram}%</p>
      <p><strong>Uptime:</strong> {uptime}</p>
      <p><strong>Crashes (24h):</strong> {stats.crashes_last_24h}</p>

      <h3>Crash Heatmap (Last 24h)</h3>
      <div style={{ display: "flex", gap: "4px" }}>
        {Array.from({ length: 24 }).map((_, i) => {
          const hourAgo = Date.now() - i * 3600 * 1000;
          const count = stats.crash_timestamps.filter(t => t * 1000 > hourAgo).length;

          return (
            <div
              key={i}
              style={{
                width: "20px",
                height: "20px",
                background: count > 0 ? "#ff4444" : "#88ff88",
                borderRadius: "4px"
              }}
              title={`${24 - i}h ago: ${count} crashes`}
            />
          );
        })}
      </div>
    </div>
  );
}
