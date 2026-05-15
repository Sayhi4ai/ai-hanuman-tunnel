import { api } from "./client";

export interface GoalEntry {
  goal: any;
  status: string;
  priority: number;
  iterations: number;
  task: any;
}

export type GoalsMap = Record<string, GoalEntry>;
export type PlansMap = Record<string, any>;

export async function fetchGoals(): Promise<GoalsMap> {
  const res = await api.get("/system/goals");
  return res.data;
}

export async function fetchPlans(): Promise<PlansMap> {
  const res = await api.get("/system/plans");
  return res.data;
}

export async function createGoal(goal: any): Promise<{ id: string }> {
  const res = await api.post("/system/goals", goal);
  return res.data;
}
