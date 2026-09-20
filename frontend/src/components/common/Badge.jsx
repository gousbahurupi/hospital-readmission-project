const TONES = {
  low: "bg-risk-lowBg text-risk-low",
  medium: "bg-risk-midBg text-risk-mid",
  high: "bg-risk-highBg text-risk-high",
  neutral: "bg-teal-50 text-teal-600"
};

export function Badge({ tone = "neutral", children }) {
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-sm text-sm font-medium ${TONES[tone]}`}>
      {children}
    </span>
  );
}
