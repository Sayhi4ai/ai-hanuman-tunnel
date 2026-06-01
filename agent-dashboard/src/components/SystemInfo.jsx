import { useEffect, useState } from "react";
import { getSystemInfo } from "../api/api";

export default function SystemInfo() {
  const [info, setInfo] = useState("");

  useEffect(() => {
    getSystemInfo().then((res) =>
      setInfo(JSON.stringify(res.data, null, 2))
    );
    API.get("/system/openclaw-version").then(res => {
      setInfo(prev => prev + "\nOpenClaw Version: " + res.data.version);
    });
  }, []);

  return (
    <div>
      <h2>System Info</h2>
      <pre style={{ background: "#222", color: "#0f0", padding: "1rem" }}>
        {info}
      </pre>
    </div>
  );
}
