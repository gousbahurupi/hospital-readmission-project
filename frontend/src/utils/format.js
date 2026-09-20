export function toPercent(score) {
  if (typeof score !== "number") return "—";
  return `${Math.round(score * 100)}%`;
}

export function riskLevelFromScore(score) {
  if (score >= 0.66) return "high";
  if (score >= 0.33) return "medium";
  return "low";
}

export function titleCase(value) {
  return value
    .replace(/[_-]/g, " ")
    .replace(/\w\S*/g, (w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase());
}
