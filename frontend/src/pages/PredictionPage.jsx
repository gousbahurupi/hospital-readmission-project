import { TopBar } from "../components/layout/TopBar.jsx";
import { Card } from "../components/common/Card.jsx";
import { PatientForm } from "../components/forms/PatientForm.jsx";
import { RiskGauge } from "../components/results/RiskGauge.jsx";
import { ExplanationPanel } from "../components/results/ExplanationPanel.jsx";
import { usePrediction } from "../hooks/usePrediction.js";
import { Link } from "react-router-dom";

export function PredictionPage() {
  const { status, prediction, explanation, error, run } = usePrediction();

  return (
    <div className="flex-1 flex flex-col">
      <TopBar title="New assessment" subtitle="Fields marked required are needed to generate a score." />
      <div className="p-8 grid grid-cols-5 gap-5">
        <Card title="Patient details" className="col-span-3">
          <PatientForm onSubmit={run} disabled={status === "loading"} />
        </Card>

        <div className="col-span-2 space-y-5">
          <Card title="Risk score" eyebrow="Prediction">
            {status === "idle" && (
              <p className="text-sm text-ink/50">Submit the form to see a risk score here.</p>
            )}
            {status === "loading" && <p className="text-sm text-ink/50">Scoring patient…</p>}
            {status === "error" && (
              <p className="text-sm text-risk-high">{error}</p>
            )}
            {status === "success" && prediction && (
              <RiskGauge riskScore={prediction.riskScore} riskLevel={prediction.riskLevel} />
            )}
          </Card>

          {status === "success" && explanation && (
            <Card title="Explanation" eyebrow="Why this score">
              <ExplanationPanel explanation={explanation} />
            </Card>
          )}

          {status === "success" && (
            <Link
              to="/agent"
              className="block text-center text-sm font-medium text-teal-500 hover:text-teal-600 border border-line rounded-sm py-2.5 bg-white"
            >
              Ask the agent about this result →
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
