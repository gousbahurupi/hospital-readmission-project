import { useEffect, useState } from "react";
import { api } from "../../services/api.js";

export function TopBar({ title, subtitle }) {
  const [connected, setConnected] = useState(null); // null = checking

  useEffect(() => {
    let cancelled = false;
    api
      .checkHealth()
      .then(() => !cancelled && setConnected(true))
      .catch(() => !cancelled && setConnected(false));
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <header className="flex items-start justify-between px-8 py-6 border-b border-line">
      <div>
        <h1 className="font-display text-2xl text-ink">{title}</h1>
        {subtitle && <p className="text-sm text-ink/60 mt-1 max-w-prose">{subtitle}</p>}
      </div>
      <div className="flex items-center gap-2 text-xs text-ink/60 pt-1.5">
        <span
          className={`h-2 w-2 rounded-full ${
            connected === null ? "bg-ink/20" : connected ? "bg-risk-low" : "bg-risk-high"
          }`}
        />
        {connected === null ? "Checking backend…" : connected ? "Backend connected" : "Backend unreachable"}
      </div>
    </header>
  );
}
