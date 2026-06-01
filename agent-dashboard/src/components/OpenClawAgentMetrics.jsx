import { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import API from "../api/api";

export default function OpenClawAgentMetrics() {
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    const load = () => {
      API.get("/system/agent-metrics").then(res => setAgents(res.data.agents));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{ padding: "1rem", background: "#eefaf5", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>Agent Performance (Last 5m)</h2>
      <BarChart width={700} height={300} data={agents}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="agent" hide />
        <YAxis />
        <Tooltip />
        <Bar dataKey="calls" fill="#8884d8" name="Calls" />
      </BarChart>
      <pre style={{ fontSize: "12px", marginTop: "0.5rem" }}>
        {agents.map(a =>
          `${a.agent} — calls: ${a.calls}, avg: ${(a.avg_duration * 1000).toFixed(1)}ms, errors: ${a.error_rate.toFixed(1)}%\n`
        )}
      </pre>
    </div>
  );
}
