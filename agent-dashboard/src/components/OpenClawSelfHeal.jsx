import { useState, useEffect } from "react";
import API from "../api/api";

export default function OpenClawSelfHeal() {
  const [status, setStatus] = useState({ enabled: true, last_action: null });

  useEffect(() => {
    const load = () => {
      API.get("/system/openclaw-selfheal").then(res => setStatus(res.data));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{ padding: "1rem", background: "#e8fff0", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>OpenClaw Self‑Healing</h2>
      <p><strong>Enabled:</strong> {status.enabled ? "Yes" : "No"}</p>
      <p><strong>Last Action:</strong> {status.last_action || "None yet"}</p>
      <p style={{ fontSize: "12px", marginTop: "0.5rem" }}>
        If the gateway dies, the watchdog will auto‑restart it every 30 seconds.
      </p>
    </div>
  );
}
