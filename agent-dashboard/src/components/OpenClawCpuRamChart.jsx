import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import API from "../api/api";

export default function OpenClawCpuRamChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const load = () => {
      API.get("/system/metrics").then(res => {
        setData(prev => [...prev.slice(-60), {
          time: new Date(res.data.timestamp * 1000).toLocaleTimeString(),
          cpu: res.data.cpu,
          ram: res.data.ram
        }]);
      });
    };

    load();
    const interval = setInterval(load, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "1rem", background: "#eef", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>CPU & RAM (Live)</h2>
      <LineChart width={600} height={300} data={data}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="time" />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Line type="monotone" dataKey="cpu" stroke="#ff4444" name="CPU %" />
        <Line type="monotone" dataKey="ram" stroke="#4444ff" name="RAM %" />
      </LineChart>
    </div>
  );
}
