export default function OpenClawDependencyMap() {
  return (
    <div style={{ padding: "1rem", background: "#eef7ff", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>OpenClaw Dependency Map</h2>

      <pre style={{ fontSize: "14px" }}>
{`
OpenClaw Gateway
 ├── Agent Runtime (uvicorn)
 │    ├── runtime_api.py
 │    ├── planner.py
 │    ├── agents/*
 │    └── supervisor.py
 ├── Dashboard (React)
 │    ├── App.jsx
 │    ├── components/*
 │    └── api/api.js
 └── System Services
      ├── systemd (openclaw-gateway.service)
      ├── /var/log/syslog
      └── Node.js (v25.8.1)
`}
      </pre>
    </div>
  );
}
