import { useState, useEffect } from "react";
import API from "../api/api";

export default function OpenClawPanel() {
  const [health, setHealth] = useState("unknown");
  const [version, setVersion] = useState("loading...");
  const [logs, setLogs] = useState([]);
  const [upgrading, setUpgrading] = useState(false);
  const [restarting, setRestarting] = useState(false);

  // Load health + version
  useEffect(() => {
    API.get("/system/openclaw-health").then(res => setHealth(res.data.status));
    API.get("/system/openclaw-version").then(res => setVersion(res.data.version));
  }, []);

  // Load logs
  const loadLogs = () => {
    API.get("/system/openclaw-logs").then(res => setLogs(res.data.logs || []));
  };

  return (
    <div style={{ padding: "1rem", background: "#eef", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>OpenClaw Gateway Panel</h2>

      <p><strong>Status:</strong> {health}</p>
      <p><strong>Version:</strong> {version}</p>

      <button
        onClick={() => {
          setRestarting(true);
          API.post("/system/openclaw-restart").then(() => {
            setRestarting(false);
            setHealth("restarting...");
            setTimeout(() => {
              API.get("/system/openclaw-health").then(res => setHealth(res.data.status));
            }, 3000);
          });
        }}
        disabled={restarting}
      >
        {restarting ? "Restarting..." : "Restart OpenClaw"}
      </button>

      <button
        onClick={() => {
          setUpgrading(true);
          API.post("/system/openclaw-upgrade").then(() => {
            setUpgrading(false);
            API.get("/system/openclaw-version").then(res => setVersion(res.data.version));
          });
        }}
        disabled={upgrading}
        style={{ marginLeft: "1rem" }}
      >
        {upgrading ? "Upgrading..." : "Upgrade OpenClaw"}
      </button>

      <hr />

      <button onClick={loadLogs}>Load OpenClaw Logs</button>

      <pre style={{ background: "#222", color: "#0f0", padding: "1rem", marginTop: "1rem" }}>
        {logs.join("\n")}
      </pre>
    </div>
  );
}
