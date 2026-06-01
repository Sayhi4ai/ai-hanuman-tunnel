import { useEffect, useState } from "react";
import { getAgents } from "../api/api";

export default function AgentList({ onSelect }) {
  const [agents, setAgents] = useState([]);
  const [turbo, setTurbo] = useState(false);

  useEffect(() => {
    getAgents().then((res) => setAgents(res.data));
    API.get("/system/mode").then(res => setTurbo(res.data.turbo_mode));
  }, []);

  return (
    <div>
      <h2>Agents</h2>
      <select onChange={(e) => onSelect(e.target.value)}>
        <option value="">Select an agent</option>
        {agents
          .filter(a => !turbo || [
            "planner",
            "backup_writer",
            "reasoning_agent",
            "browser",
            "filereader",
            "queue_manager",
            "queue_worker",
            "manager_agent",
            "supervisor"
          ].includes(a))
          .map(a => (
            <option key={a} value={a}>{a}</option>
        ))}
      </select>
    </div>
  );
}
