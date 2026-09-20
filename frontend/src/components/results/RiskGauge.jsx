import { Badge } from "../common/Badge.jsx";
import { toPercent } from "../../utils/format.js";

const LEVEL_COPY = {
  low: "Standard discharge planning is likely sufficient.",
  medium: "Consider a follow-up call within 7 days and a medication review.",
  high: "Recommend care-coordination referral before discharge."
};

export function RiskGauge({ riskScore, riskLevel }) {
  const pct = Math.round((riskScore ?? 0) * 100);
  const trackColor = { low: "#4C7A4A", medium: "#B8862E", high: "#B3452F" }[riskLevel] || "#2C5F5A";

  return (
    <div className="flex items-center gap-6">
      <div className="relative h-28 w-28 shrink-0">
        <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90">
          <circle cx="50" cy="50" r="42" fill="none" stroke="#EAF1EF" strokeWidth="10" />
          <circle
            cx="50"
            cy="50"
            r="42"
            fill="none"
            stroke={trackColor}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={`${2 * Math.PI * 42}`}
            strokeDashoffset={`${2 * Math.PI * 42 * (1 - pct / 100)}`}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="font-display text-2xl text-ink">{toPercent(riskScore)}</span>
          <span className="text-[11px] text-ink/50">30-day risk</span>
        </div>
      </div>
      <div className="space-y-2">
        <Badge tone={riskLevel}>{riskLevel === "high" ? "High risk" : riskLevel === "medium" ? "Moderate risk" : "Low risk"}</Badge>
        <p className="text-sm text-ink/70 max-w-xs">{LEVEL_COPY[riskLevel] || ""}</p>
      </div>
    </div>
  );
}
