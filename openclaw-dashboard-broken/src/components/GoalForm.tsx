import React, { useState } from "react";
import { createGoal } from "../api/system";

interface Props {
  onCreated?: () => void;
}

export const GoalForm: React.FC<Props> = ({ onCreated }) => {
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setBusy(true);
    try {
      await createGoal({ description: text.trim() });
      setText("");
      onCreated?.();
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="flex gap-2">
      <input
        className="flex-1 bg-slate-900 border border-slate-700 rounded px-2 py-1 text-sm text-slate-100"
        placeholder="Describe a new goal..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        type="submit"
        disabled={busy}
        className="px-3 py-1 text-sm rounded bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50"
      >
        {busy ? "Creating..." : "Create"}
      </button>
    </form>
  );
};
