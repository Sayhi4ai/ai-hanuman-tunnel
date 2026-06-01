import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:7200",
});

export const getAgents = () => API.get("/agents");
export const runAgent = (agent, task) =>
  API.post("/run-agent", { agent, task });

export const getMemory = () => API.get("/system/memory");
export const getQueue = () => API.get("/system/queue");
export const getLogs = () => API.get("/system/logs");
export const getSystemInfo = () => API.get("/system/info");

export default API;
