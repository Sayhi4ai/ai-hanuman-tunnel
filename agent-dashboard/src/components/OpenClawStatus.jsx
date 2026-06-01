import { useState, useEffect } from "react";
import API from "../api/api";

export default function OpenClawStatus() {
  const [status, setStatus] = useState("unknown");

  useEffect(() => {
    API.get("/system/openclaw-health").then(res => {
      setStatus(res.data.status);
    });
  }, []);

  return (
    <div style={{ padding: "10px", background: "#eef", marginBottom: "1rem" }}>
      OpenClaw Gateway Status: <strong>{status}</strong>
    </div>
  );
}
