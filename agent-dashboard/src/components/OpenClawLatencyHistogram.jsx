import { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import API from "../api/api";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function OpenClawLatencyHistogram() {
  const [buckets, setBuckets] = useState([0, 0, 0, 0, 0]);

  useEffect(() => {
    const load = () => {
      API.get("/system/openclaw-rps").then(res => {
        const hist = [0, 0, 0, 0, 0];
        res.data.history.forEach(h => {
          const ms = h.duration * 1000;
          if (ms < 100) hist[0]++;
          else if (ms < 300) hist[1]++;
          else if (ms < 700) hist[2]++;
          else if (ms < 1500) hist[3]++;
          else hist[4]++;
        });
        setBuckets(hist);
      });
    };
    load();
    const id = setInterval(load, 2000);
    return () => clearInterval(id);
  }, []);

  const data = {
    labels: ["<100ms", "100–300ms", "300–700ms", "700–1500ms", ">1500ms"],
    datasets: [
      {
        label: "Requests",
        data: buckets,
        backgroundColor: "rgba(54, 162, 235, 0.6)",
      },
    ],
  };

  return (
    <div style={{ padding: "1rem", background: "#f5f5ff", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>Latency Histogram (Last 60s)</h2>
      <Bar data={data} />
    </div>
  );
}
