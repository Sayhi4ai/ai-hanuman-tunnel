import React, { useEffect, useState } from "react";
import { systemSocket } from "../ws/systemSocket";

interface EventItem {
  ts: string;
  payload: any;
}

export const EventStream: React.FC = () => {
  const [events, setEvents] = useState<EventItem[]>([]);

  useEffect(() => {
    const unsubscribe = systemSocket.subscribe((evt) => {
      setEvents((prev) => [
        { ts: new Date().toISOString(), payload: evt },
        ...prev.slice(0, 99),
      ]);
    });

    return unsubscribe;
  }, []);

  return (
    <div className="bg-slate-900 rounded-lg p-4 h-full">
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-lg font-semibold">Event Stream</h2>
        <span className="text-xs text-slate-400">{events.length} events</span>
      </div>

      <div className="space-y-2 max-h-80 overflow-auto text-xs">
        {events.length === 0 && (
          <div className="text-slate-500">No events yet.</div>
        )}

        {events.map((e, idx) => (
          <div
            key={idx}
            className="border border-slate-700 rounded-md p-2"
          >
            <div className="text-[10px] text-slate-500 mb-1">{e.ts}</div>

            <pre className="whitespace-pre-wrap text-slate-200">
              {JSON.stringify(e.payload, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    </div>
  );
};
