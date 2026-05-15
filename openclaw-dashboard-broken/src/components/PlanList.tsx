import React from "react";
import type { PlansMap } from "../api/system";

interface Props {
  plans: PlansMap;
}

export const PlanList: React.FC<Props> = ({ plans }) => {
  const entries = Object.entries(plans);

  return (
    <div className="bg-slate-900 rounded-lg p-4 h-full">
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-lg font-semibold">Plans</h2>
        <span className="text-xs text-slate-400">{entries.length} total</span>
      </div>

      <div className="space-y-2 max-h-80 overflow-auto">
        {entries.length === 0 && (
          <div className="text-sm text-slate-500">No plans yet.</div>
        )}

        {entries.map(([id, p]) => (
          <div
            key={id}
            className="border border-slate-700 rounded-md p-2 text-sm"
          >
            <div className="flex justify-between mb-1">
              <span className="font-mono text-xs text-slate-400 truncate">
                {id}
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800">
                {p.status ?? "unknown"}
              </span>
            </div>

            <pre className="text-xs text-slate-200 whitespace-pre-wrap">
              {JSON.stringify(p, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    </div>
  );
};
