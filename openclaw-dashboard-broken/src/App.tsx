import React, { useEffect, useState } from "react";
import { fetchGoals, fetchPlans, GoalsMap, PlansMap } from "./api/system";
import { GoalList } from "./components/GoalList";
import { PlanList } from "./components/PlanList";
import { GoalForm } from "./components/GoalForm";
import { EventStream } from "./components/EventStream";

const App: React.FC = () => {
  const [goals, setGoals] = useState<GoalsMap>({});
  const [plans, setPlans] = useState<PlansMap>({});
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const [g, p] = await Promise.all([fetchGoals(), fetchPlans()]);
      setGoals(g);
      setPlans(p);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-slate-800 px-6 py-3 flex justify-between items-center bg-slate-950/80">
        <div>
          <h1 className="text-xl font-semibold">OpenClaw Ops Dashboard</h1>
          <p className="text-xs text-slate-400">
            Backend: http://localhost:8081 · WS: /system/ws
          </p>
        </div>
        <button
          onClick={load}
          className="px-3 py-1 text-sm rounded bg-slate-800 hover:bg-slate-700"
        >
          {loading ? "Refreshing..." : "Refresh"}
        </button>
      </header>

      <main className="flex-1 px-6 py-4 grid grid-cols-3 gap-4">
        <section className="col-span-2 flex flex-col gap-3">
          <div className="bg-slate-900 rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-3">New Goal</h2>
            <GoalForm onCreated={load} />
          </div>
          <GoalList goals={goals} />
        </section>

        <section className="col-span-1 flex flex-col gap-3">
          <PlanList plans={plans} />
          <EventStream />
        </section>
      </main>
    </div>
  );
};

export default App;
