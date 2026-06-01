import { useState, useEffect } from "react";
import API from "../api/api";

export default function TurboSwitch() {
  const [turbo, setTurbo] = useState(false);

  useEffect(() => {
    API.get("/system/mode").then(res => setTurbo(res.data.turbo_mode));
  }, []);

  const toggle = async () => {
    const newState = !turbo;
    setTurbo(newState);
    await API.post("/system/mode", { turbo_mode: newState });
  };

  return (
    <div style={{ marginBottom: "1rem" }}>
      <label style={{ fontSize: "1.2rem" }}>
        <input
          type="checkbox"
          checked={turbo}
          onChange={toggle}
          style={{ marginRight: "0.5rem" }}
        />
        Turbo Mode
      </label>
    </div>
  );
}
