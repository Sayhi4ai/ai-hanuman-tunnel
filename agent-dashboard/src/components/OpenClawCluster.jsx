import { useState, useEffect } from "react";
import API from "../api/api";

export default function OpenClawCluster() {
  const [nodes, setNodes] = useState([]);

  useEffect(() => {
    const load = () => {
      API.get("/system/cluster-nodes").then(res => setNodes(res.data.nodes));
    };
    load();
    const id = setInterval(load, 3000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{ padding: "1rem", background: "#eef7ff", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>Distributed Agent Cluster</h2>
      <pre style={{ fontSize: "12px" }}>
        {nodes.map(n =>
          `${n.id} (${n.role}) — ${n.status} — latency=${n.latency_ms || "N/A"}ms\n`
        )}
      </pre>
    </div>
  );
}
