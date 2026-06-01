import { useEffect, useState } from "react";
import { getMemory } from "../api/api";

export default function MemoryViewer() {
  const [memory, setMemory] = useState("");

  useEffect(() => {
    getMemory().then((res) =>
      setMemory(JSON.stringify(res.data, null, 2))
    );
  }, []);

  return (
    <div>
      <h2>Memory</h2>
      <pre style={{ background: "#222", color: "#0f0", padding: "1rem" }}>
        {memory}
      </pre>
    </div>
  );
}
