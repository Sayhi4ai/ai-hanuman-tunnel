import { useEffect, useState } from "react";
import API from "../api/api";

export default function LogsViewer() {
  const [activeTab, setActiveTab] = useState("System Logs");
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    if (activeTab === "System Logs") {
      API.get("/system/logs").then(res => setLogs(res.data.logs || []));
    }

    if (activeTab === "OpenClaw Logs") {
      API.get("/system/openclaw-logs").then(res => setLogs(res.data.logs || []));
    }
  }, [activeTab]);

  return (
    <div>
      <h2>Logs</h2>

      {/* Tabs */}
      <div style={{ marginBottom: "1rem" }}>
        <button onClick={() => setActiveTab("System Logs")}>
          System Logs
        </button>
        <button onClick={() => setActiveTab("OpenClaw Logs")}>
          OpenClaw Logs
        </button>
      </div>

      {/* Log Output */}
      <pre style={{ background: "#222", color: "#0f0", padding: "1rem" }}>
        {logs.join("\n")}
      </pre>
    </div>
  );
}
