export function ExplanationPanel({ explanation }) {
  if (!explanation) return null;
  const { summary, contributions = [], recommendations = [] } = explanation;

  return (
    <div className="space-y-5">
      {summary && <p className="text-sm text-ink/80 leading-relaxed">{summary}</p>}

      {contributions.length > 0 && (
        <div>
          <h3 className="text-xs font-semibold text-ink/50 uppercase tracking-wide mb-2">
            Contributing factors
          </h3>
          <ul className="space-y-2">
            {contributions.map((c, i) => (
              <li key={i} className="flex items-start gap-2 text-sm">
                <span
                  className={`mt-1.5 h-1.5 w-1.5 rounded-full shrink-0 ${
                    c.direction === "increases" ? "bg-risk-high" : "bg-risk-low"
                  }`}
                />
                <span>
                  <span className="font-medium text-ink">{c.factor}</span>{" "}
                  <span className="text-ink/60">
                    {c.direction === "increases" ? "increases" : "lowers"} risk — {c.detail}
                  </span>
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {recommendations.length > 0 && (
        <div>
          <h3 className="text-xs font-semibold text-ink/50 uppercase tracking-wide mb-2">
            Suggested next steps
          </h3>
          <ul className="space-y-1.5">
            {recommendations.map((r, i) => (
              <li key={i} className="text-sm text-ink/80 pl-4 border-l-2 border-teal-100">
                {r}
              </li>
            ))}
          </ul>
        </div>
      )}
      {explanation.disclaimer && <p className="border-t border-line pt-3 text-xs leading-relaxed text-ink/50">{explanation.disclaimer}</p>}
    </div>
  );
}
