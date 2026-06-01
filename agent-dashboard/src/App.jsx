import { useState, useEffect } from "react";
import API from "./api/api";

import AgentList from "./components/AgentList";
import AgentRunner from "./components/AgentRunner";
import MemoryViewer from "./components/MemoryViewer";
import QueueViewer from "./components/QueueViewer";
import LogsViewer from "./components/LogsViewer";
import SystemInfo from "./components/SystemInfo";
import TurboSwitch from "./components/TurboSwitch";
import OpenClawStatus from "./components/OpenClawStatus";
import OpenClawPanel from "./components/OpenClawPanel";
import OpenClawMonitor from "./components/OpenClawMonitor";
import OpenClawRPSChart from "./components/OpenClawRPSChart";
import OpenClawErrorGraph from "./components/OpenClawErrorGraph";
import OpenClawDependencyMap from "./components/OpenClawDependencyMap";
import OpenClawCpuRamChart from "./components/OpenClawCpuRamChart";
import OpenClawCpuRamChart from "./components/OpenClawCpuRamChart";
import OpenClawLatencyHistogram from "./components/OpenClawLatencyHistogram";
import OpenClawAgentMetrics from "./components/OpenClawAgentMetrics";
import OpenClawCallGraph from "./components/OpenClawCallGraph";
import OpenClawTimeline from "./components/OpenClawTimeline";
import OpenClawErrorHeatmap from "./components/OpenClawErrorHeatmap";
import OpenClawSelfHeal from "./components/OpenClawSelfHeal";
import OpenClawPlannerBrain from "./components/OpenClawPlannerBrain";
import OpenClawCluster from "./components/OpenClawCluster";

export default function App() {
  const [selectedAgent, setSelectedAgent] = useState("");
  const [turbo, setTurbo] = useState(false);

  // Load Turbo Mode state when dashboard loads
  useEffect(() => {
    API.get("/system/mode").then(res => {
      setTurbo(res.data.turbo_mode);
    });
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "system-ui" }}>
      <h1>Agent Runtime Dashboard</h1>

      {/* Turbo Mode Indicator */}
      <div
        style={{
          padding: "10px",
          marginBottom: "1rem",
          background: turbo ? "#ffcccc" : "#ccffcc",
          borderRadius: "8px",
          fontWeight: "bold"
        }}
      >
        {turbo ? "🚀 TURBO MODE ACTIVE" : "🟢 Normal Mode"}
      </div>

      {/* Turbo Mode Switch */}
      <TurboSwitch />
      <OpenClawStatus />
      <OpenClawPanel />
      <OpenClawMonitor />
      <OpenClawRPSChart />
      <OpenClawErrorGraph />
      <OpenClawDependencyMap />
      <OpenClawCpuRamChart />
      <OpenClawCpuRamChart />
      <OpenClawLatencyHistogram />
      <OpenClawAgentMetrics />
      <OpenClawCallGraph />
      <OpenClawTimeline />
      <OpenClawErrorHeatmap />
      <OpenClawSelfHeal />
      <OpenClawPlannerBrain />
      <OpenClawCluster />

      <button onClick={() => API.post("/system/openclaw-restart")}>
        Restart OpenClaw Gateway
      </button>
      <button onClick={() => API.post("/system/openclaw-upgrade")}>
        Upgrade OpenClaw
      </button>

      {/* Agent Controls */}
      <AgentList onSelect={setSelectedAgent} />
      <AgentRunner agent={selectedAgent} />

      <hr />

      {/* System Panels */}
      <SystemInfo />
      <MemoryViewer />
      <QueueViewer />
      <LogsViewer />
    </div>
  );
}
