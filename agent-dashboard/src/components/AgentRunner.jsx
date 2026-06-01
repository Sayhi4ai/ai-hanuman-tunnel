import { useState } from "react";
import { runAgent } from "../api/api";

export default function AgentRunner({ agent }) {
  const [task, setTask] = useState("");
  const [result, setResult] = useState("");

  const execute = async () => {
    const res = await runAgent(agent, task);
    setResult(JSON.stringify(res.data, null, 2));
  };

  return (
    <div>
      <h2>Run Agent</h2>
      <textarea
        rows={4}
        style={{ width: "100%" }}
        placeholder="Enter task..."
        value={task}
        onChange={(e) => setTask(e.target.value)}
      />
      <button onClick={execute} disabled={!agent}>
        Run
      </button>

      <pre style={{ background: "#111", color: "#0f0", padding: "1rem" }}>
        {result || "// No output yet"}
      </pre>
    </div>
  );
}
