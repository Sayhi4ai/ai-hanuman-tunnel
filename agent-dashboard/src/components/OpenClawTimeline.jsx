import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import API from "../api/api";

export default function OpenClawTimeline() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const load = () => {
      API.get("/system/openclaw-timeline").then(res => {
        const mapped = res.data.events.map(e => ({
          time: new Date(e.timestamp * 1000).toLocaleTimeString(),
          value: e.type === "restart" ? 2 : e.type === "error" ? 1 : 0,
          label: e.detail,
        }));
        setEvents(mapped);
      });
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{ padding: "1rem", background: "#fff7ee", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>OpenClaw Performance Timeline</h2>
      <LineChart width={700} height={250} data={events}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="time" />
        <YAxis ticks={[0, 1, 2]} />
        <Tooltip />
        <Line type="stepAfter" dataKey="value" stroke="#ff8800" />
      </LineChart>
      <pre style={{ fontSize: "12px", marginTop: "0.5rem" }}>
        {events.map(e => `${e.time} — ${e.label}\n`)}
      </pre>
    </div>
  );
}
