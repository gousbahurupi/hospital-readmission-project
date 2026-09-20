import { useEffect, useState } from "react";
import { TopBar } from "../components/layout/TopBar.jsx";
import { Card } from "../components/common/Card.jsx";
import { api } from "../services/api.js";

export function ModelInfoPage() {
  const [info, setInfo] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .getModelInfo()
      .then(setInfo)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div className="flex-1 flex flex-col">
      <TopBar title="About the model" subtitle="Version, training data, and known limitations." />
      <div className="p-8 max-w-prose">
        <Card>
          {error && <p className="text-sm text-risk-high">{error}</p>}
          {!error && !info && <p className="text-sm text-ink/50">Loading model information…</p>}
          {info && (
            <dl className="space-y-4 text-sm">
              <div>
                <dt className="text-xs font-semibold text-ink/50 uppercase tracking-wide">Version</dt>
                <dd className="text-ink">{info.version || "—"}</dd>
              </div>
              <div>
                <dt className="text-xs font-semibold text-ink/50 uppercase tracking-wide">Trained on</dt>
                <dd className="text-ink">{info.trainingData || "—"}</dd>
              </div>
              <div>
                <dt className="text-xs font-semibold text-ink/50 uppercase tracking-wide">Known limitations</dt>
                <dd className="text-ink/80">{info.limitations || "—"}</dd>
              </div>
            </dl>
          )}
        </Card>
      </div>
    </div>
  );
}
