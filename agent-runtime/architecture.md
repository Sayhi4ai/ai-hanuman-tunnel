flowchart TD
  subgraph Core["Core Runtime"]
    Q[Task Queue]
    R[Agent Registry]
    M[Vector Memory]
    LB[Load Balancer]
  end

  subgraph CoreAgents["Core Agents"]
    PL[planner_agent]
    WR[writer_agent]
    RE[reasoning_agent]
  end

  subgraph Advanced["Advanced Agents"]
    SW[swarm_agent]
    GE[genetic_agent]
    CH[chaos_agent]
  end

  subgraph Governance["Governance & Safety"]
    GOV[governance_agent]
    ETH[ethics_agent]
    THR[threat_agent]
    SEC[security_agent]
  end

  subgraph Distributed["Distributed & Mesh"]
    DIST[distributed_agent]
    MESH[mesh_agent]
    FED[federation_agent]
    DIP[diplomacy_agent]
  end

  Q --> LB
  LB --> R
  LB --> PL
  LB --> WR
  LB --> RE

  PL --> SW
  RE --> SW
  SW --> GE

  PL --> GOV
  WR --> GOV
  RE --> GOV

  GOV --> ETH
  GOV --> THR
  THR --> SEC

  PL --> DIST
  WR --> DIST
  RE --> DIST

  DIST --> MESH
  MESH --> FED
  FED --> DIP

  M --> PL
  M --> WR
  M --> RE
