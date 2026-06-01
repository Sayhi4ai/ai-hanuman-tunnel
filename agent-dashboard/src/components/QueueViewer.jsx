import { useEffect, useState } from "react";
import { getQueue } from "../api/api";

export default function QueueViewer() {
  const [queue, setQueue] = useState("");

  useEffect(() => {
    getQueue().then((res) =>
      setQueue(JSON.stringify(res.data, null, 2))
    );
  }, []);

  return (
    <div>
      <h2>Queue</h2>
      <pre style={{ background: "#222", color: "#0f0", padding: "1rem" }}>
        {queue}
      </pre>
    </div>
  );
}
