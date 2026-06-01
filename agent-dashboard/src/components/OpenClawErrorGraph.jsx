import { useState, useEffect } from "react";
import API from "../api/api";

export default function OpenClawErrorGraph() {
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    const load = () => {
      API.get("/system/openclaw-rps").then(res => {
        const points = res.data.history.map(h => h.status >= 400 ? 1 : 0);
        setErrors(points);
      });
    };

    load();
    const interval = setInterval(load, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "1rem", background: "#ffe", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>Error Rate (Last 60s)</h2>

      <div style={{ display: "flex", gap: "2px", height: "60px", alignItems: "flex-end" }}>
        {errors.map((e, i) => (
          <div
            key={i}
            style={{
              width: "4px",
              height: `${e * 60}px`,
              background: e ? "#ff0000" : "#cccccc"
            }}
          />
        ))}
      </div>
    </div>
  );
}
