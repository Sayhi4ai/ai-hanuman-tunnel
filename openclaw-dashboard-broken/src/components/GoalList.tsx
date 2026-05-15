import React from "react";
import type { GoalsMap } from "../api/system";

interface Props {
  goals: GoalsMap;
}

export const GoalList: React.FC<Props> = ({ goals }) => {
  const entries = Object.entries(goals);

  return (
    <div className="bg-slate-900 rounded-lg p-4 h-full">
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-lg font-semibold">Goals</h2>
        <span className="text-xs text-slate-400">{entries.length} total</span>
      </div>

      <div className="space-y-2 max-h-80 overflow-auto">
        {entries.length === 0 && (
          <div className="text-sm text-slate-500">No goals yet.</div>
        )}

        {entries.map(([id, g]) => (
          <div
            key={id}
            className="border border-slate-700 rounded-md p-2 text-sm flex flex-col gap-1"
          >
            <div className="flex justify-between">
              <span className="font-mono text-xs text-slate-400 truncate">
                {id}
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800">
                {g.status}
              </span>
            </div>

            <div className="text-slate-200">
              {JSON.stringify(g.goal)}
            </div>

            <div className="text-xs text-slate-500">
              priority {g.priority} · iterations {g.iterations}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
